"""
Router de Usuarios.
Endpoints para gestionar usuarios en la plataforma.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from collections import Counter

from app.database import get_session
from app.models import Usuario, Favorito, Pelicula
from app.schemas import (
    UsuarioCreate,
    UsuarioRead,
    UsuarioUpdate,
    PeliculaRead
)

# Crear el router con prefijo y tags
router = APIRouter(
    prefix="/api/usuarios",
    tags=["Usuarios"]
)


# Endpoint para listar todos los usuarios
@router.get("/", response_model=List[UsuarioRead])
def listar_usuarios(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    """
    Lista todos los usuarios registrados.
    
    - **skip**: Número de registros a omitir (para paginación)
    - **limit**: Número máximo de registros a retornar
    """
    # Consultar todos los usuarios con paginación
    usuarios = session.exec(select(Usuario).offset(skip).limit(limit)).all()
    return usuarios


# Endpoint para crear un nuevo usuario
@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario: UsuarioCreate,
    session: Session = Depends(get_session)
):
    """
    Crea un nuevo usuario en la plataforma.
    
    - **nombre**: Nombre del usuario
    - **correo**: Correo electrónico único
    """
    # Verificar que el correo no exista
    existing_user = session.exec(
        select(Usuario).where(
            Usuario.correo == usuario.correo
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )
    
    # Crear el nuevo usuario
    db_usuario = Usuario.model_validate(usuario)
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)
    
    return db_usuario


# Endpoint para obtener un usuario por ID
@router.get("/{usuario_id}", response_model=UsuarioRead)
def obtener_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    """
    Obtiene un usuario específico por su ID.
    
    - **usuario_id**: ID del usuario
    """
    # Buscar el usuario por ID
    usuario = session.get(Usuario, usuario_id)
    #si no se encuentra el usuario
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )
    return usuario


# Endpoint para actualizar un usuario
@router.put("/{usuario_id}", response_model=UsuarioRead)
def actualizar_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    session: Session = Depends(get_session)
):
    """
    Actualiza la información de un usuario existente.
    
    - **usuario_id**: ID del usuario a actualizar
    - **nombre**: Nuevo nombre (opcional)
    - **correo**: Nuevo correo (opcional)
    """
    # Buscar el usuario
    db_usuario = session.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        ) 
    
    # Si se actualiza el correo, verificar que no exista
    if usuario_update.correo and usuario_update.correo != db_usuario.correo:
        existing_user = session.exec(
            select(Usuario).where(
                Usuario.correo == usuario_update.correo
            )
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo ya está registrado"
            )
    # Actualizar solo los campos proporcionados
    usuario_data = usuario_update.model_dump(exclude_unset=True)
    for key, value in usuario_data.items():
        setattr(db_usuario, key, value)
    session.add(db_usuario)
    session.commit()
    session.refresh(db_usuario)
    
    return db_usuario


#  Endpoint para eliminar un usuario
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    """
    Elimina un usuario de la plataforma.
    
    - **usuario_id**: ID del usuario a eliminar
    
    También se eliminarán todos los favoritos asociados al usuario.
    """
    # Buscar el usuario
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )
    
    # Eliminar los favoritos asociados al usuario primero
    statement = select(Favorito).where(Favorito.id_usuario == usuario_id)
    favoritos_a_eliminar = session.exec(statement).all()
    for favorito in favoritos_a_eliminar:
        session.delete(favorito)

    # Ahora eliminar el usuario
    session.delete(usuario)
    session.commit()
    return None


#  Endpoint para obtener los favoritos de un usuario
@router.get("/{usuario_id}/favoritos", response_model=List[PeliculaRead])
def listar_favoritos_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    """
    Lista todas las películas favoritas de un usuario.
    
    - **usuario_id**: ID del usuario
    """
    #  Verificar que el usuario existe
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )
    
    #  Obtener las películas favoritas del usuario
    statement = select(Pelicula).join(Favorito).where(Favorito.id_usuario == usuario_id)
    
    # Ejecutar la consulta
    peliculas = session.exec(statement).all()
    
    return peliculas


#  Endpoint para marcar una película como favorita
@router.post(
    "/{usuario_id}/favoritos/{pelicula_id}",
    status_code=status.HTTP_201_CREATED
)
def marcar_favorito(
    usuario_id: int,
    pelicula_id: int,
    session: Session = Depends(get_session)
):
    """
    Marca una película como favorita para un usuario.
    
    - **usuario_id**: ID del usuario
    - **pelicula_id**: ID de la película
    """
    # Verificar que el usuario existe
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )
    
    # Verificar que la película existe
    pelicula = session.get(Pelicula, pelicula_id)
    if not pelicula:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Película con id {pelicula_id} no encontrada"
        )
   
    # Verificar si ya existe el favorito
    statement = select(Favorito).where(
        Favorito.id_usuario == usuario_id,
        Favorito.id_pelicula == pelicula_id
    )
    existing_favorito = session.exec(statement).first()
    if existing_favorito:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La película ya está marcada como favorita"
        )
    
    #  Crear el favorito
    favorito = Favorito(
        id_usuario=usuario_id,
        id_pelicula=pelicula_id
    )
    session.add(favorito)
    session.commit()
    session.refresh(favorito)
    
    return {"message": "Película marcada como favorita exitosamente"}


# Endpoint para eliminar una película de favoritos
@router.delete(
    "/{usuario_id}/favoritos/{pelicula_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_favorito(
    usuario_id: int,
    pelicula_id: int,
    session: Session = Depends(get_session)
):
    """
    Elimina una película de los favoritos de un usuario.
    
    - **usuario_id**: ID del usuario
    - **pelicula_id**: ID de la película
    """
    # Buscar el favorito
    statement = select(Favorito).where(
        Favorito.id_usuario == usuario_id,
        Favorito.id_pelicula == pelicula_id
    )
    favorito = session.exec(statement).first()
    
    if not favorito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El favorito no existe"
        )
    
    # Eliminar el favorito
    session.delete(favorito)
    session.commit()
    
    return None


# Opcional - Endpoint para estadísticas del usuario
@router.get("/{usuario_id}/estadisticas")
def obtener_estadisticas_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    """
    Obtiene estadísticas del usuario (películas favoritas, géneros preferidos, etc.)
    
    - **usuario_id**: ID del usuario
    """
    # Verificar que el usuario existe
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {usuario_id} no encontrado"
        )

    # Obtener las películas favoritas del usuario para calcular las estadísticas
    statement = select(Pelicula).join(Favorito).where(Favorito.id_usuario == usuario_id)
    peliculas = session.exec(statement).all()

    # Calcular número total de favoritos
    total_favoritos = len(peliculas)
        
    # Obtener géneros más favoritos
    generos = []
    for pelicula in peliculas:
        if pelicula.genero:
            generos.extend([g.strip() for g in pelicula.genero.split(",")])

    
    generos_counter = Counter(generos)
    generos_comunes = generos_counter.most_common(3)
    # Calcular tiempo total de películas favoritas
    tiempo_total = sum(p.duracion for p in peliculas if p.duracion)
    
    return {
        "usuario_id": usuario_id,
        "total_peliculas_favoritas": total_favoritos,
        "generos_preferidos": [{"genero": g[0], "cantidad": g[1]} for g in generos_comunes],
        "tiempo_total_minutos": tiempo_total,
        "tiempo_total_formateado": f"{tiempo_total // 60}h {tiempo_total % 60}m" if tiempo_total else "0m"
    }

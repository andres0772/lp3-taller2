-- ============================================
-- Script SQL para poblar la base de datos
-- Base de datos: SQLite (peliculas.db)
-- ============================================

-- Insertar 5 Usuarios
INSERT INTO usuario (nombre, correo, fecha_registro) VALUES
('María García', 'maria.garcia@email.com', datetime('now')),
('Juan Pérez', 'juan.perez@email.com', datetime('now')),
('Ana Martínez', 'ana.martinez@email.com', datetime('now')),
('Carlos Rodríguez', 'carlos.rodriguez@email.com', datetime('now')),
('Laura Fernández', 'laura.fernandez@email.com', datetime('now'));

-- Insertar 10 Películas
INSERT INTO pelicula (titulo, director, genero, duracion, año, clasificacion, sinopsis, fecha_creacion) VALUES
('El Padrino', 'Francis Ford Coppola', 'Drama, Crimen', 175, 1972, 'R',
 'La historia de una familia mafiosa italiana y su lucha por mantener el poder en el mundo del crimen organizado.',
 datetime('now')),
('Inception', 'Christopher Nolan', 'Ciencia Ficción, Acción', 148, 2010, 'PG-13',
 'Un ladrón que roba secretos corporativos mediante el uso de tecnología de sueños compartidos recibe la tarea inversa de plantar una idea.',
 datetime('now')),
('Pulp Fiction', 'Quentin Tarantino', 'Crimen, Drama', 154, 1994, 'R',
 'Las vidas de dos sicarios, un boxeador, la esposa de un gánster y dos bandidos se entrelazan en cuatro historias de violencia y redención.',
 datetime('now')),
('Forrest Gump', 'Robert Zemeckis', 'Drama, Romance', 142, 1994, 'PG-13',
 'Las décadas de vida de Forrest Gump, un hombre con buen corazón pero limitaciones intelectuales, que presencia eventos históricos importantes.',
 datetime('now')),
('Matrix', 'Lana Wachowski, Lilly Wachowski', 'Ciencia Ficción, Acción', 136, 1999, 'R',
 'Un hacker descubre que la realidad tal como la conocemos es una simulación creada por máquinas inteligentes.',
 datetime('now')),
('El Señor de los Anillos: El Retorno del Rey', 'Peter Jackson', 'Fantasía, Aventura', 201, 2003, 'PG-13',
 'Gandalf y Aragorn lideran el mundo de los hombres contra el ejército de Sauron para distraer su atención de Frodo y Sam.',
 datetime('now')),
('Interestelar', 'Christopher Nolan', 'Ciencia Ficción, Drama', 169, 2014, 'PG-13',
 'Un equipo de exploradores viaja a través de un agujero de gusano en el espacio para asegurar la supervivencia de la humanidad.',
 datetime('now')),
('Parásitos', 'Bong Joon-ho', 'Drama, Thriller', 132, 2019, 'R',
 'La codicia y la discriminación de clases amenazan la relación simbiótica recién formada entre la rica familia Park y el clan Kim.',
 datetime('now')),
('El Caballero de la Noche', 'Christopher Nolan', 'Acción, Drama', 152, 2008, 'PG-13',
 'Cuando el Joker emerge para sembrar el caos en Gotham City, Batman debe aceptar una de las pruebas psicológicas y físicas más grandes.',
 datetime('now')),
('La La Land', 'Damien Chazelle', 'Romance, Musical', 128, 2016, 'PG-13',
 'Mientras se esfuerzan por triunfar en sus carreras artísticas, un pianista de jazz y una aspirante a actriz se enamoran.',
 datetime('now'));

-- Insertar algunos favoritos de ejemplo
INSERT INTO favorito (id_usuario, id_pelicula, fecha_marcado) VALUES
(1, 1, datetime('now')),
(1, 5, datetime('now')),
(2, 2, datetime('now')),
(2, 9, datetime('now')),
(3, 10, datetime('now')),
(4, 3, datetime('now')),
(4, 8, datetime('now')),
(5, 6, datetime('now')),
(5, 7, datetime('now'));

-- Verificar los datos insertados
SELECT * FROM usuario;
SELECT id, titulo, director, año, genero FROM pelicula;
SELECT f.id, u.nombre AS usuario, p.titulo AS pelicula, f.fecha_marcado
  FROM favorito f
  JOIN usuario u ON f.id_usuario = u.id
  JOIN pelicula p ON f.id_pelicula = p.id;

-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 03-11-2024 a las 14:03:02
-- Versión del servidor: 8.0.31
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `botdb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `acciones`
--

DROP TABLE IF EXISTS `acciones`;
CREATE TABLE IF NOT EXISTS `acciones` (
  `idacciones` int NOT NULL AUTO_INCREMENT,
  `accion` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idacciones`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `acciones`
--

INSERT INTO `acciones` (`idacciones`, `accion`) VALUES
(1, 'Consultar Fechas.'),
(2, 'Inscribirse en los exámenes.'),
(3, 'Realizar Reclamo.'),
(4, 'Consultar Inscripciones.'),
(5, 'Consultar Reclamos.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carreras`
--

DROP TABLE IF EXISTS `carreras`;
CREATE TABLE IF NOT EXISTS `carreras` (
  `idCarrera` int NOT NULL AUTO_INCREMENT,
  `Carrera` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`idCarrera`),
  UNIQUE KEY `Carrera` (`Carrera`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `carreras`
--

INSERT INTO `carreras` (`idCarrera`, `Carrera`) VALUES
(1, 'Tecnicatura Superior en Análisis de Sistemas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `correlativas`
--

DROP TABLE IF EXISTS `correlativas`;
CREATE TABLE IF NOT EXISTS `correlativas` (
  `idMateria` int NOT NULL,
  `idCorrelativa` int NOT NULL,
  PRIMARY KEY (`idMateria`,`idCorrelativa`),
  KEY `idCorrelativa` (`idCorrelativa`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `correlativas`
--

INSERT INTO `correlativas` (`idMateria`, `idCorrelativa`) VALUES
(9, 6),
(9, 7),
(10, 4),
(11, 5),
(11, 8),
(12, 2),
(13, 6),
(13, 7),
(14, 4),
(15, 8),
(16, 3),
(17, 16),
(19, 6),
(19, 10),
(21, 12),
(22, 10),
(22, 11),
(22, 14),
(22, 15),
(23, 15);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

DROP TABLE IF EXISTS `estudiantes`;
CREATE TABLE IF NOT EXISTS `estudiantes` (
  `idEstudiante` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `dni` varchar(20) DEFAULT NULL,
  `celular` varchar(30) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `idCarrera` int DEFAULT NULL,
  `idUsuario` int DEFAULT NULL,
  PRIMARY KEY (`idEstudiante`),
  UNIQUE KEY `dni` (`dni`),
  KEY `idCarrera` (`idCarrera`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`idEstudiante`, `nombre`, `apellido`, `dni`, `celular`, `email`, `idCarrera`, `idUsuario`) VALUES
(1, 'Sergio', 'Genevrino', '22708446', '2235328067', 'sergiogenevrino666@gmail.com', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `examenes`
--

DROP TABLE IF EXISTS `examenes`;
CREATE TABLE IF NOT EXISTS `examenes` (
  `id_examen` int NOT NULL AUTO_INCREMENT,
  `dia_examen` varchar(12) NOT NULL,
  `fecha_examen` date NOT NULL,
  `hora_examen` time NOT NULL,
  `id_materia` int NOT NULL,
  `observaciones` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_examen`),
  KEY `id_materia` (`id_materia`)
) ENGINE=MyISAM AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `examenes`
--

INSERT INTO `examenes` (`id_examen`, `dia_examen`, `fecha_examen`, `hora_examen`, `id_materia`, `observaciones`) VALUES
(1, 'Lunes', '2024-11-25', '17:30:00', 1, 'Virtual'),
(2, 'Lunes', '2024-11-25', '19:40:00', 2, NULL),
(3, 'Martes', '2024-11-26', '18:00:00', 3, NULL),
(4, 'Miercoles', '2024-11-27', '17:30:00', 5, 'Grupo A'),
(5, 'Miercoles', '2024-11-27', '19:40:00', 5, 'Grupo B'),
(6, 'Jueves', '2024-11-28', '17:30:00', 6, NULL),
(7, 'Jueves', '2024-11-28', '17:30:00', 7, NULL),
(8, 'Viernes', '2024-11-29', '17:30:00', 4, NULL),
(9, 'Viernes', '2024-11-29', '19:40:00', 8, NULL),
(10, 'Lunes', '2024-12-02', '17:30:00', 13, NULL),
(11, 'Lunes', '2024-12-02', '19:40:00', 10, NULL),
(12, 'Martes', '2024-12-03', '17:30:00', 11, 'Grupo A - Virtual'),
(13, 'Martes', '2024-12-03', '19:30:00', 11, 'Grupo B - Virtual'),
(14, 'Miercoles', '2024-12-04', '17:30:00', 9, NULL),
(15, 'Jueves', '2024-12-05', '17:30:00', 12, NULL),
(16, 'Jueves', '2024-12-05', '19:40:00', 14, 'Virtual'),
(17, 'Viernes', '2024-12-06', '17:30:00', 15, 'Virtual'),
(18, 'Viernes', '2024-12-06', '19:40:00', 16, NULL),
(19, 'Lunes', '2024-12-09', '17:30:00', 17, NULL),
(20, 'Lunes', '2024-12-09', '19:40:00', 18, NULL),
(21, 'Martes', '2024-12-10', '17:30:00', 19, 'Virtual'),
(22, 'Miercoles', '2024-12-11', '17:30:00', 23, 'Virtual'),
(23, 'Miercoles', '2024-12-11', '19:40:00', 21, NULL),
(24, 'Jueves', '2024-12-12', '17:30:00', 20, 'Virtual'),
(25, 'Viernes', '2024-12-13', '19:40:00', 22, 'Virtual');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `examen_profesor`
--

DROP TABLE IF EXISTS `examen_profesor`;
CREATE TABLE IF NOT EXISTS `examen_profesor` (
  `id_examen` int NOT NULL,
  `id_profesor` int NOT NULL,
  KEY `id_examen` (`id_examen`),
  KEY `id_profesor` (`id_profesor`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `examen_profesor`
--

INSERT INTO `examen_profesor` (`id_examen`, `id_profesor`) VALUES
(1, 1),
(1, 3),
(1, 10),
(2, 2),
(2, 1),
(3, 3),
(4, 3),
(4, 12),
(4, 7),
(5, 3),
(5, 1),
(5, 12),
(6, 4),
(6, 5),
(6, 3),
(7, 5),
(7, 4),
(7, 3),
(8, 1),
(8, 12),
(8, 3),
(9, 6),
(9, 1),
(9, 9),
(10, 1),
(10, 3),
(11, 1),
(11, 11),
(11, 2),
(12, 3),
(13, 3),
(13, 1),
(14, 7),
(14, 12),
(14, 3),
(15, 5),
(15, 4),
(15, 12),
(16, 3),
(16, 5),
(16, 1),
(17, 3),
(17, 1),
(17, 12),
(18, 9),
(18, 6),
(19, 10),
(19, 1),
(19, 3),
(20, 11),
(20, 2),
(21, 1),
(21, 3),
(22, 12),
(22, 9),
(22, 3),
(23, 13),
(23, 1),
(23, 12),
(24, 12),
(24, 5),
(24, 4),
(25, 3),
(25, 6),
(25, 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupos`
--

DROP TABLE IF EXISTS `grupos`;
CREATE TABLE IF NOT EXISTS `grupos` (
  `idgrupos` int NOT NULL AUTO_INCREMENT,
  `grupo` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idgrupos`),
  UNIQUE KEY `idgrupos_UNIQUE` (`idgrupos`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `grupos`
--

INSERT INTO `grupos` (`idgrupos`, `grupo`) VALUES
(1, 'Estudiante'),
(2, 'Preceptor');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inscripciones_examenes`
--

DROP TABLE IF EXISTS `inscripciones_examenes`;
CREATE TABLE IF NOT EXISTS `inscripciones_examenes` (
  `id_inscripcion` int NOT NULL AUTO_INCREMENT,
  `id_estudiante` int NOT NULL,
  `id_examen` int NOT NULL,
  `fecha_inscripcion` date DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'pendiente',
  PRIMARY KEY (`id_inscripcion`),
  KEY `id_estudiante` (`id_estudiante`),
  KEY `id_examen` (`id_examen`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `inscripciones_examenes`
--

INSERT INTO `inscripciones_examenes` (`id_inscripcion`, `id_estudiante`, `id_examen`, `fecha_inscripcion`, `estado`) VALUES
(3, 1, 21, '2024-11-03', 'pendiente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

DROP TABLE IF EXISTS `materias`;
CREATE TABLE IF NOT EXISTS `materias` (
  `idMateria` int NOT NULL AUTO_INCREMENT,
  `Materia` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `periodo` int NOT NULL,
  `idCarrera` int NOT NULL,
  PRIMARY KEY (`idMateria`),
  UNIQUE KEY `Materia` (`Materia`),
  KEY `idCarrera` (`idCarrera`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `materias`
--

INSERT INTO `materias` (`idMateria`, `Materia`, `periodo`, `idCarrera`) VALUES
(1, 'Ciencia, Tecnología y Sociedad', 1, 1),
(2, 'Ingles I', 1, 1),
(3, 'Arquitectura de los Computadores', 1, 1),
(4, 'Algoritmos y Estructuras de Datos I', 1, 1),
(5, 'Practicas Profesionalizantes I', 1, 1),
(6, 'Análisis Matemático I', 1, 1),
(7, 'Algebra', 1, 1),
(8, 'Sistemas y Organizaciones', 1, 1),
(9, 'Estadística', 2, 1),
(10, 'Algoritmos y Estructuras de Datos II', 2, 1),
(11, 'Practicas Profesionalizantes II', 2, 1),
(12, 'Ingles II', 2, 1),
(13, 'Análisis Matemático II', 2, 1),
(14, 'Base de Datos', 2, 1),
(15, 'Ingeniería de Software I', 2, 1),
(16, 'Sistemas Operativos', 2, 1),
(17, 'Redes y Comunicaciones', 3, 1),
(18, 'Aspectos Legales de la Profesión', 3, 1),
(19, 'Algoritmos y Estructuras de Datos III', 3, 1),
(20, 'Seminario', 3, 1),
(21, 'Ingles III', 3, 1),
(22, 'Practicas Profesionalizantes III', 3, 1),
(23, 'Ingeniería de Software II', 3, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materiascursadas`
--

DROP TABLE IF EXISTS `materiascursadas`;
CREATE TABLE IF NOT EXISTS `materiascursadas` (
  `idMateriaCursada` int NOT NULL AUTO_INCREMENT,
  `idEstudiante` int NOT NULL,
  `idMateria` int NOT NULL,
  `idStatusMateria` int NOT NULL,
  `fecha` year NOT NULL,
  PRIMARY KEY (`idMateriaCursada`),
  KEY `idEstudiante` (`idEstudiante`),
  KEY `idMateria` (`idMateria`),
  KEY `idStatusMateria` (`idStatusMateria`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `materiascursadas`
--

INSERT INTO `materiascursadas` (`idMateriaCursada`, `idEstudiante`, `idMateria`, `idStatusMateria`, `fecha`) VALUES
(1, 1, 1, 5, 2022),
(2, 1, 2, 5, 2022),
(3, 1, 3, 5, 2022),
(4, 1, 4, 5, 2022),
(5, 1, 5, 5, 2022),
(6, 1, 6, 5, 2022),
(7, 1, 7, 5, 2022),
(8, 1, 8, 5, 2022),
(9, 1, 9, 5, 2023),
(10, 1, 10, 5, 2023),
(11, 1, 11, 5, 2023),
(12, 1, 12, 5, 2023),
(13, 1, 13, 5, 2023),
(14, 1, 14, 5, 2022),
(15, 1, 15, 5, 2023),
(16, 1, 16, 4, 2023),
(17, 1, 17, 5, 2023),
(18, 1, 18, 1, 2024),
(19, 1, 19, 2, 2024),
(20, 1, 20, 2, 2024),
(21, 1, 21, 3, 2024),
(22, 1, 22, 5, 2022),
(23, 1, 23, 2, 2024);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

DROP TABLE IF EXISTS `permisos`;
CREATE TABLE IF NOT EXISTS `permisos` (
  `idgrupos` int DEFAULT NULL,
  `idacciones` int DEFAULT NULL,
  KEY `idgrupos_idx` (`idgrupos`),
  KEY `idacciones_idx` (`idacciones`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`idgrupos`, `idacciones`) VALUES
(1, 1),
(1, 2),
(1, 3),
(2, 4),
(2, 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

DROP TABLE IF EXISTS `profesores`;
CREATE TABLE IF NOT EXISTS `profesores` (
  `idProfesor` int NOT NULL AUTO_INCREMENT,
  `Profesor` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`idProfesor`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `profesores`
--

INSERT INTO `profesores` (`idProfesor`, `Profesor`) VALUES
(1, 'Jose Oemig'),
(2, 'Nadia Dezzuto'),
(3, 'Gabriel Gonzalez Ferreira'),
(4, 'Graciela Noya'),
(5, 'Julio Riera'),
(6, 'Juan Manuel Arrascada'),
(7, 'Stella Figueroa'),
(8, 'Gabriela Ferreiro'),
(9, 'Gabriel Pimentel'),
(10, 'Hernan Hinojal'),
(11, 'Sofia Giménez Iraola'),
(12, 'Matias Gaston Santiago'),
(13, 'Luciana Costa');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reclamos`
--

DROP TABLE IF EXISTS `reclamos`;
CREATE TABLE IF NOT EXISTS `reclamos` (
  `id_reclamo` int NOT NULL AUTO_INCREMENT,
  `id_estudiante` int NOT NULL,
  `fecha_reclamo` date DEFAULT NULL,
  `motivo` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `estado` varchar(20) DEFAULT 'pendiente',
  `respuesta` text,
  `fecha_respuesta` date DEFAULT NULL,
  PRIMARY KEY (`id_reclamo`),
  KEY `id_estudiante` (`id_estudiante`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `reclamos`
--

INSERT INTO `reclamos` (`id_reclamo`, `id_estudiante`, `fecha_reclamo`, `motivo`, `estado`, `respuesta`, `fecha_respuesta`) VALUES
(1, 1, NULL, 'Anotame en Base de datos', 'pendiente', NULL, NULL),
(2, 1, '2024-11-02', 'Anotame', 'pendiente', NULL, NULL),
(3, 1, '2024-11-02', 'No estoy anotado en Ingles II', 'pendiente', NULL, NULL),
(4, 1, '2024-11-02', 'No estoy en estadistica', 'pendiente', NULL, NULL),
(5, 1, '2024-11-02', 'shit', 'pendiente', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `statusmaterias`
--

DROP TABLE IF EXISTS `statusmaterias`;
CREATE TABLE IF NOT EXISTS `statusmaterias` (
  `idStatusMateria` int NOT NULL AUTO_INCREMENT,
  `estadoMateria` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`idStatusMateria`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `statusmaterias`
--

INSERT INTO `statusmaterias` (`idStatusMateria`, `estadoMateria`) VALUES
(1, 'No Cursada'),
(2, 'Cursando'),
(3, 'Cursada Aprobada'),
(4, 'Cursada  No Aprobada'),
(5, 'Aprobada'),
(6, 'Aprobada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuariogrupo`
--

DROP TABLE IF EXISTS `usuariogrupo`;
CREATE TABLE IF NOT EXISTS `usuariogrupo` (
  `idusuarios` int DEFAULT NULL,
  `idgrupos` int DEFAULT NULL,
  KEY `idusuarios_idx` (`idusuarios`),
  KEY `idgrupos_idx` (`idgrupos`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `usuariogrupo`
--

INSERT INTO `usuariogrupo` (`idusuarios`, `idgrupos`) VALUES
(1, 1),
(2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `idusuarios` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `password` varchar(62) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`idusuarios`),
  UNIQUE KEY `idusuarios_UNIQUE` (`idusuarios`),
  UNIQUE KEY `usuario` (`usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idusuarios`, `usuario`, `password`) VALUES
(1, 'Sergio', '$2b$12$86K/3CeLQhfZvdmaA5OHAeWX/Rqy2IHUPRi9fHbkEe2eq6hjqVkbe'),
(2, 'Jose', '$2b$12$UJHjy/cJtl2YvzpGGxYmDuhSOfDat9Iv9qLTPhgRPzSFwKBeNTmde'),
(3, 'Luis', '$2b$12$yo52GFECVBLfApoEgwsrT..Qm0INRdaRA7JWjr47ktNU03k1O8hq2'),
(4, 'Carlos', '$2b$12$oyAjqGWyn4Cm.KzwWW2S8OOw4NhrrelqzE0TXu35vO.2xyMZbxgs6');

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD CONSTRAINT `idacciones` FOREIGN KEY (`idacciones`) REFERENCES `acciones` (`idacciones`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `idgruposaccion` FOREIGN KEY (`idgrupos`) REFERENCES `grupos` (`idgrupos`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `usuariogrupo`
--
ALTER TABLE `usuariogrupo`
  ADD CONSTRAINT `idgrupos` FOREIGN KEY (`idgrupos`) REFERENCES `grupos` (`idgrupos`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `idusuarios` FOREIGN KEY (`idusuarios`) REFERENCES `usuarios` (`idusuarios`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

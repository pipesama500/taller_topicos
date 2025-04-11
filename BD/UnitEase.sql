CREATE DATABASE IF NOT EXISTS unitease;
USE unitease;

-- Tabla de Roles
CREATE TABLE Roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Tabla de Usuarios
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    id_apartamento INT,
    FOREIGN KEY (id_rol) REFERENCES Roles(id),
    FOREIGN KEY (id_apartamento) REFERENCES Apartamentos(id)
);

-- Tabla de Unidades Residenciales
CREATE TABLE Unidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE Torres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_unidad INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_unidad) REFERENCES Unidades(id)
);

CREATE TABLE Pisos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_torre INT NOT NULL,
    numero INT NOT NULL,
    FOREIGN KEY (id_torre) REFERENCES Torres(id)
);

CREATE TABLE Apartamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_piso INT NOT NULL,
    numero INT NOT NULL,
    FOREIGN KEY (id_piso) REFERENCES Pisos(id)
);

-- Tabla de Visitas
CREATE TABLE Visitas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_apartamento INT NOT NULL,
    nombre_visitante VARCHAR(100) NOT NULL,
    fecha_visita DATE NOT NULL,
    hora_visita TIME NOT NULL,
    es_frecuente BOOLEAN NOT NULL,
    fecha_expiracion_frecuente DATE,
    qr_code VARCHAR(255),
    FOREIGN KEY (id_apartamento) REFERENCES Apartamentos(id)
);

-- Tabla de Domicilios
CREATE TABLE Domicilios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_apartamento INT NOT NULL,
    proveedor VARCHAR(100) NOT NULL,
    nombre_producto VARCHAR(100),
    nombre_repartidor VARCHAR(100),
    fecha_anuncio DATE NOT NULL,
    personalizado BOOLEAN NOT NULL,
    FOREIGN KEY (id_apartamento) REFERENCES Apartamentos(id)
);

-- Tabla de Paquetes
CREATE TABLE Paquetes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_apartamento INT NOT NULL,
    proveedor VARCHAR(100) NOT NULL,
    nombre_producto VARCHAR(100),
    nombre_repartidor VARCHAR(100),
    fecha_anuncio DATE NOT NULL,
    fecha_estimacion DATE,
    personalizado BOOLEAN NOT NULL,
    FOREIGN KEY (id_apartamento) REFERENCES Apartamentos(id)
);

-- Tabla de Zonas Comunes
CREATE TABLE Zonas_Comunes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de Reservas
CREATE TABLE Reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_zona_comun INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_reserva DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    FOREIGN KEY (id_zona_comun) REFERENCES Zonas_Comunes(id),
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

-- Tabla de Publicaciones
CREATE TABLE Publicaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    fecha_publicacion DATE NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id)
);

-- Tabla de Chats
CREATE TABLE Chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario_emisor INT NOT NULL,
    id_usuario_receptor INT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario_emisor) REFERENCES Usuarios(id),
    FOREIGN KEY (id_usuario_receptor) REFERENCES Usuarios(id)
);

-- Crear base de datos
CREATE DATABASE TiendaVirtualRopa;
USE TiendaVirtualRopa;

-- Tabla Roles
CREATE TABLE Roles (
    RolID INT NOT NULL AUTO_INCREMENT,
    Nombre VARCHAR(100) NOT NULL,
    PRIMARY KEY (RolID)
);

-- Tabla Usuarios
CREATE TABLE Usuarios (
    UsuarioID INT NOT NULL AUTO_INCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE,
    Contrasena VARCHAR(255) NOT NULL,
    Telefono VARCHAR(50),
    RolID INT NOT NULL,
    PRIMARY KEY (UsuarioID),
    FOREIGN KEY (RolID) REFERENCES Roles(RolID)
);

-- Tabla Clientes
CREATE TABLE Clientes (
    ClienteID INT NOT NULL AUTO_INCREMENT,
    UsuarioID INT NOT NULL,
    FechaRegistro DATETIME NOT NULL,
    Estado BIT NOT NULL,
    PRIMARY KEY (ClienteID),
    FOREIGN KEY (UsuarioID) REFERENCES Usuarios(UsuarioID)
);

-- Tabla Direcciones
CREATE TABLE Direcciones (
    DireccionID INT NOT NULL AUTO_INCREMENT,
    ClienteID INT NOT NULL,
    Calle VARCHAR(255) NOT NULL,
    Ciudad VARCHAR(100) NOT NULL,
    Barrio VARCHAR(100),
    CodigoPostal VARCHAR(20),
    PRIMARY KEY (DireccionID),
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID)
);

-- Tabla Categorías
CREATE TABLE Categorias (
    CategoriaID INT NOT NULL AUTO_INCREMENT,
    NombreCategoria VARCHAR(100) NOT NULL,
    Descripcion TEXT,
    PRIMARY KEY (CategoriaID)
);

-- Tabla Marcas
CREATE TABLE Marcas (
    MarcaID INT NOT NULL AUTO_INCREMENT,
    NombreMarca VARCHAR(100) NOT NULL,
    PaisOrigen VARCHAR(100),
    PRIMARY KEY (MarcaID)
);

-- Tabla Productos
CREATE TABLE Productos (
    ProductoID INT NOT NULL AUTO_INCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Precio DECIMAL(10,2) NOT NULL,
    Stock INT NOT NULL,
    CategoriaID INT NOT NULL,
    MarcaID INT NOT NULL,
    PRIMARY KEY (ProductoID),
    FOREIGN KEY (CategoriaID) REFERENCES Categorias(CategoriaID),
    FOREIGN KEY (MarcaID) REFERENCES Marcas(MarcaID)
);

-- Tabla Variantes de Producto
CREATE TABLE VariantesProducto (
    VarianteID INT NOT NULL AUTO_INCREMENT,
    ProductoID INT NOT NULL,
    Talla VARCHAR(10),
    Color VARCHAR(50),
    SKU VARCHAR(100),
    PRIMARY KEY (VarianteID),
    FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID)
);

-- Tabla Carritos
CREATE TABLE Carritos (
    CarritoID INT NOT NULL AUTO_INCREMENT,
    ClienteID INT NOT NULL,
    FechaCreacion DATETIME NOT NULL,
    Activo BIT NOT NULL,
    PRIMARY KEY (CarritoID),
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID)
);

-- Tabla CarritoDetalle
CREATE TABLE CarritoDetalle (
    CarritoDetalleID INT NOT NULL AUTO_INCREMENT,
    CarritoID INT NOT NULL,
    ProductoID INT NOT NULL,
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (CarritoDetalleID),
    FOREIGN KEY (CarritoID) REFERENCES Carritos(CarritoID),
    FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID)
);

-- Tabla Métodos de Pago
CREATE TABLE MetodoPago (
    MetodoPagoID INT NOT NULL AUTO_INCREMENT,
    NombreMetodo VARCHAR(100) NOT NULL,
    PRIMARY KEY (MetodoPagoID)
);

-- Tabla Pedidos
CREATE TABLE Pedidos (
    PedidoID INT NOT NULL AUTO_INCREMENT,
    ClienteID INT NOT NULL,
    FechaPedido DATETIME NOT NULL,
    EstadoPedido VARCHAR(50) NOT NULL,
    MetodoPagoID INT NOT NULL,
    PRIMARY KEY (PedidoID),
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID),
    FOREIGN KEY (MetodoPagoID) REFERENCES MetodoPago(MetodoPagoID)
);

-- Tabla PedidoDetalle
CREATE TABLE PedidoDetalle (
    PedidoDetalleID INT NOT NULL AUTO_INCREMENT,
    PedidoID INT NOT NULL,
    ProductoID INT NOT NULL,
    Cantidad INT NOT NULL,
    PrecioUnitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (PedidoDetalleID),
    FOREIGN KEY (PedidoID) REFERENCES Pedidos(PedidoID),
    FOREIGN KEY (ProductoID) REFERENCES Productos(ProductoID)
);

-- Tabla Pagos
CREATE TABLE Pagos (
    PagoID INT NOT NULL AUTO_INCREMENT,
    PedidoID INT NOT NULL,
    FechaPago DATETIME NOT NULL,
    Monto DECIMAL(10,2) NOT NULL,
    EstadoPago VARCHAR(50) NOT NULL,
    PRIMARY KEY (PagoID),
    FOREIGN KEY (PedidoID) REFERENCES Pedidos(PedidoID)
);

-- Tabla Envios
CREATE TABLE Envios (
    EnvioID INT NOT NULL AUTO_INCREMENT,
    PedidoID INT NOT NULL,
    Transportador VARCHAR(100) NOT NULL,
    NoGuia VARCHAR(100) NOT NULL,
    FechaEnvio DATETIME NOT NULL,
    PRIMARY KEY (EnvioID),
    FOREIGN KEY (PedidoID) REFERENCES Pedidos(PedidoID)
);
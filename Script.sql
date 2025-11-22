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

INSERT INTO `roles` (`RolID`, `Nombre`) VALUES ('1', 'Admin');

INSERT INTO Categorias (NombreCategoria, Descripcion) VALUES
('Camisetas', 'Ropa superior casual para hombre y mujer.'),
('Pantalones', 'Prendas inferiores de diferentes materiales y estilos.'),
('Chaquetas', 'Ropa exterior para clima frío o lluvioso.'),
('Zapatos', 'Calzado formal, casual y deportivo.'),
('Accesorios', 'Gafas, cinturones, relojes, y otros complementos.');

INSERT INTO Marcas (NombreMarca, PaisOrigen) VALUES
('Nike', 'Estados Unidos'),
('Adidas', 'Alemania'),
('Puma', 'Alemania'),
('Levi’s', 'Estados Unidos'),
('Zara', 'España'),
('H&M', 'Suecia');

-- PROCEDIMIENTOS ALMACENADOS PARA AUTENTICACIÓN
DELIMITER //

CREATE PROCEDURE sp_create_user(
    IN p_nombre VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_contrasena VARCHAR(255),
    IN p_telefono VARCHAR(50),
    IN p_rolid INT
)
BEGIN
    INSERT INTO Usuarios (Nombre, Email, Contrasena, Telefono, RolID)
    VALUES (p_nombre, p_email, p_contrasena, p_telefono, p_rolid);
    SET @uid = LAST_INSERT_ID();
    INSERT INTO Clientes (UsuarioID, FechaRegistro, Estado)
    VALUES (@uid, NOW(), 1);
    SELECT @uid AS UsuarioID, LAST_INSERT_ID() AS ClienteID;
END;
//

CREATE PROCEDURE sp_login(
    IN p_email VARCHAR(255),
    IN p_contrasena VARCHAR(255)
)
BEGIN
    SELECT UsuarioID, Nombre, Email, Telefono, RolID
    FROM Usuarios
    WHERE Email = p_email AND Contrasena = p_contrasena
    LIMIT 1;
END;
//

CREATE PROCEDURE sp_create_user_with_cliente(
    IN p_nombre VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_contrasena VARCHAR(255),
    IN p_telefono VARCHAR(50),
    IN p_rolid INT
)
BEGIN
    INSERT INTO Usuarios (Nombre, Email, Contrasena, Telefono, RolID)
    VALUES (p_nombre, p_email, p_contrasena, p_telefono, p_rolid);

    SET @uid = LAST_INSERT_ID();

    INSERT INTO Clientes (UsuarioID, FechaRegistro, Estado)
    VALUES (@uid, NOW(), 1);

    SELECT @uid AS UsuarioID;
END;
//

CREATE PROCEDURE sp_get_all_users()
BEGIN
    SELECT U.UsuarioID, C.ClienteID, Nombre, Email, Telefono, RolID FROM Usuarios u
	left JOIN clientes C ON C.UsuarioID = U.UsuarioID;
END;
//

CREATE PROCEDURE sp_get_user_by_id(IN p_usuario_id INT)
BEGIN
    SELECT UsuarioID, Nombre, Email, Telefono, RolID FROM Usuarios WHERE UsuarioID = p_usuario_id LIMIT 1;
END;
//

CREATE PROCEDURE sp_update_user(
    IN p_usuario_id INT,
    IN p_nombre VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_contrasena VARCHAR(255),
    IN p_telefono VARCHAR(50),
    IN p_rolid INT
)
BEGIN
    UPDATE Usuarios
    SET Nombre = COALESCE(p_nombre, Nombre),
            Email = COALESCE(p_email, Email),
            Contrasena = COALESCE(p_contrasena, Contrasena),
            Telefono = COALESCE(p_telefono, Telefono),
            RolID = COALESCE(p_rolid, RolID)
    WHERE UsuarioID = p_usuario_id;
    SELECT UsuarioID, Nombre, Email, Telefono, RolID FROM Usuarios WHERE UsuarioID = p_usuario_id;
END;
//

CREATE PROCEDURE sp_delete_user(IN p_usuario_id INT)
BEGIN
    DELETE FROM Clientes WHERE UsuarioID = p_usuario_id;
    DELETE FROM Usuarios WHERE UsuarioID = p_usuario_id;
    SELECT ROW_COUNT() AS affected;
END;
//

-- PROCEDIMIENTOS PARA PRODUCTOS
CREATE PROCEDURE sp_create_product(
    IN p_nombre VARCHAR(255),
    IN p_descripcion TEXT,
    IN p_precio DECIMAL(10,2),
    IN p_stock INT,
    IN p_categoria_id INT,
    IN p_marca_id INT
)
BEGIN
    INSERT INTO Productos (Nombre, Descripcion, Precio, Stock, CategoriaID, MarcaID)
    VALUES (p_nombre, p_descripcion, p_precio, p_stock, p_categoria_id, p_marca_id);
    SELECT LAST_INSERT_ID() AS ProductoID;
END;
//

CREATE PROCEDURE sp_get_product_by_id(IN p_producto_id INT)
BEGIN
    SELECT * FROM Productos WHERE ProductoID = p_producto_id LIMIT 1;
END;
//

CREATE PROCEDURE sp_list_products()
BEGIN
    SELECT * FROM Productos;
END;
//

CREATE PROCEDURE sp_update_product(
    IN p_producto_id INT,
    IN p_nombre VARCHAR(255),
    IN p_descripcion TEXT,
    IN p_precio DECIMAL(10,2),
    IN p_stock INT,
    IN p_categoria_id INT,
    IN p_marca_id INT
)
BEGIN
    UPDATE Productos
    SET Nombre = COALESCE(p_nombre, Nombre),
            Descripcion = COALESCE(p_descripcion, Descripcion),
            Precio = COALESCE(p_precio, Precio),
            Stock = COALESCE(p_stock, Stock),
            CategoriaID = COALESCE(p_categoria_id, CategoriaID),
            MarcaID = COALESCE(p_marca_id, MarcaID)
    WHERE ProductoID = p_producto_id;
    SELECT * FROM Productos WHERE ProductoID = p_producto_id;
END;
//

CREATE PROCEDURE sp_delete_product(IN p_producto_id INT)
BEGIN
    DELETE FROM Productos WHERE ProductoID = p_producto_id;
    SELECT ROW_COUNT() AS affected;
END;
//

-- PROCEDIMIENTOS PARA CARRITO
CREATE PROCEDURE sp_get_active_cart(IN p_cliente_id INT)
BEGIN
    SELECT * FROM Carritos WHERE ClienteID = p_cliente_id AND Activo = 1 LIMIT 1;
END;
//

CREATE PROCEDURE sp_create_cart(IN p_cliente_id INT)
BEGIN
    INSERT INTO Carritos (ClienteID, FechaCreacion, Activo) VALUES (p_cliente_id, NOW(), 1);
    SELECT LAST_INSERT_ID() AS CarritoID;
END;
//

CREATE PROCEDURE sp_add_to_cart(
    IN p_carrito_id INT,
    IN p_producto_id INT,
    IN p_cantidad INT
)
BEGIN
    -- etiqueta para poder usar LEAVE
    proc: BEGIN
        DECLARE v_stock INT;

        -- Si quieres que el procedimiento inicie la transacción, descomenta:
        -- START TRANSACTION;

        SELECT Stock INTO v_stock
        FROM Productos
        WHERE ProductoID = p_producto_id
        FOR UPDATE;

        IF v_stock IS NULL THEN
            SELECT -1 AS status, 'producto_no_encontrado' AS message;
            LEAVE proc;
        END IF;

        IF v_stock < p_cantidad THEN
            SELECT -2 AS status, 'stock_insuficiente' AS message, v_stock AS available;
            LEAVE proc;
        ELSE
            INSERT INTO CarritoDetalle (CarritoID, ProductoID, Cantidad, PrecioUnitario)
            SELECT p_carrito_id, ProductoID, p_cantidad, Precio
            FROM Productos
            WHERE ProductoID = p_producto_id;

            UPDATE Productos
            SET Stock = Stock - p_cantidad
            WHERE ProductoID = p_producto_id;

            -- Si la tabla CarritoDetalle tiene AUTO_INCREMENT, LAST_INSERT_ID() devolverá su id
            SELECT LAST_INSERT_ID() AS CarritoDetalleID, 0 AS status, 'ok' AS message;
        END IF;

        -- Si el procedimiento maneja la transacción, descomenta:
        -- COMMIT;
    END proc;
END;
//

    -- obtener carrito(s) y detalles por cliente
    DELIMITER //
    CREATE PROCEDURE sp_get_cart_with_details_by_cliente(IN p_cliente_id INT)
    BEGIN
        SELECT
            c.CarritoID,
            c.ClienteID,
            c.FechaCreacion,
            c.Activo,
            cd.CarritoDetalleID,
            cd.ProductoID,
            p.Nombre AS ProductoNombre,
            cd.Cantidad,
            cd.PrecioUnitario
        FROM Carritos c
        LEFT JOIN CarritoDetalle cd ON cd.CarritoID = c.CarritoID
        LEFT JOIN Productos p ON p.ProductoID = cd.ProductoID
        WHERE c.ClienteID = p_cliente_id
        ORDER BY c.CarritoID, cd.CarritoDetalleID;
    END;
    //

    DELIMITER ;

    -- PROCEDIMIENTO PARA OBTENER UN PEDIDO CON SUS DETALLES
    DELIMITER //
    CREATE PROCEDURE sp_get_order_by_id(IN p_pedido_id INT)
    BEGIN
        SELECT
            pe.PedidoID,
            pe.ClienteID,
            pe.FechaPedido,
            pe.EstadoPedido,
            pe.MetodoPagoID,
            pd.PedidoDetalleID,
            pd.ProductoID,
            pr.Nombre AS ProductoNombre,
            pd.Cantidad,
            pd.PrecioUnitario
        FROM Pedidos pe
        LEFT JOIN PedidoDetalle pd ON pd.PedidoID = pe.PedidoID
        LEFT JOIN Productos pr ON pr.ProductoID = pd.ProductoID
        WHERE pe.PedidoID = p_pedido_id
        ORDER BY pd.PedidoDetalleID;
    END;
    //

    DELIMITER ;

    -- PROCEDIMIENTO PARA CREAR UN PEDIDO A PARTIR DE UN CARRITO
    DELIMITER //
    CREATE PROCEDURE sp_create_order_from_cart(IN p_carrito_id INT, IN p_metodo_pago_id INT)
    BEGIN
        proc: BEGIN
            DECLARE v_cliente INT;
            SELECT ClienteID INTO v_cliente FROM Carritos WHERE CarritoID = p_carrito_id LIMIT 1;
            IF v_cliente IS NULL THEN
                SELECT -1 AS status, 'carrito_no_encontrado' AS message;
                LEAVE proc;
            END IF;

            INSERT INTO Pedidos (ClienteID, FechaPedido, EstadoPedido, MetodoPagoID)
            VALUES (v_cliente, NOW(), 'Pendiente de pago', p_metodo_pago_id);
            SET @pid = LAST_INSERT_ID();

            INSERT INTO PedidoDetalle (PedidoID, ProductoID, Cantidad, PrecioUnitario)
            SELECT @pid, ProductoID, Cantidad, PrecioUnitario
            FROM CarritoDetalle
            WHERE CarritoID = p_carrito_id;

            DELETE FROM CarritoDetalle WHERE CarritoID = p_carrito_id;

            UPDATE Carritos SET Activo = 0 WHERE CarritoID = p_carrito_id;

            SELECT @pid AS PedidoID, 0 AS status, 'ok' AS message;
        END proc;
    END;
    //

    DELIMITER ;

    -- PROCEDIMIENTO PARA VACIAR UN CARRITO Y RESTAURAR STOCK
    DELIMITER //
    CREATE PROCEDURE sp_empty_cart_by_id(IN p_carrito_id INT)
    BEGIN
        -- Actualizar el stock sumando las cantidades del detalle
        UPDATE Productos p
        JOIN CarritoDetalle cd ON cd.ProductoID = p.ProductoID
        SET p.Stock = p.Stock + cd.Cantidad
        WHERE cd.CarritoID = p_carrito_id;

        -- Eliminar los detalles del carrito
        DELETE FROM CarritoDetalle WHERE CarritoID = p_carrito_id;

        -- Marcar carrito como inactivo
        DELETE FROM Carritos WHERE CarritoID = p_carrito_id;

        SELECT ROW_COUNT() AS deleted_details;
    END;
    //

    DELIMITER ;

# Api de ordenes

## Endpoints


| Endpoint             | Método | Descripción                              |                               
| -------------------- | ------ | ---------------------------------------- |
| `/orders`            | GET    | Obtener todos los pedidos                |
| `/orders`            | POST   | Crear un nuevo pedido.                   | 
| `/orders/{order_id}` | GET    | Obtener detalles de un pedido específico.| 
| `/orders/{order_id}` | DELETE | Eliminar un pedido.                      | 

```json
{
    "id_usuario": 3,
    "products": [{
        "id_produt": 3,
        "quantity": 4
    }]
}
```


TODO
- Modificar db a sqlAlchemy
    - C4ncino/hackaton_ibero

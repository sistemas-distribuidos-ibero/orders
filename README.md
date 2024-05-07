# API de ordenes

## Enpoints

| Endpoint | Metodo | Descripcion |
|------|-----| ----|
| /orders | GET | Get all orders | 
| /orders/<id> | GET | Get order by id | 


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
- Documentar endpoints
- .gitignore
    - gitignore.io
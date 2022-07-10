<h1 align="center">
  <br>
  <br>
  Proyecto 2 de Base de Datos 2
  <br>
</h1>
<p align="center">
  <img src="https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white">
  <img src="https://img.shields.io/badge/CLion-black?style=for-the-badge&logo=clion&logoColor=white">
  <img src="https://img.shields.io/badge/NeoVim-%2357A143.svg?&style=for-the-badge&logo=neovim&logoColor=white">
  <img src="https://img.shields.io/badge/CMake-%23008FBA.svg?style=for-the-badge&logo=cmake&logoColor=white">
  <img src="https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white">
</p>
<!-- 
TODO: colocar el gif
<h1 align="center">
  <a href="#"><img src="./assets/capture.gif" alt="" width="70%"></a>
</h1> -->


## Integrantes

| Apellidos y Nombres       | Código de alumno | % Participación |
|---------------------------|------------------|-----------------|
| Morales Panitz, Alexander | 202020195        | 100%            |
| Ugarte Quispe, Grover     | 202020159        | 100%            |
| Gutierrez Guanilo, Luis   | 202010074        | 100%            |

# Enlace a video: 

## Librerías utilizadas

### Listado de librerías

Para la interfaz requerimos:
- Flask: manipulación de web

Para aplicar los métodos listados, es necesario contar con las siguientes liberías.

- heapq: Permite operaciones de una cola de prioridades
- face_recognition: Nos permite procesar archivos de imágenes y retornarlas como vectores (codificación)
- numpy: Nos permite manipular imágenes como vectores, además las liberías siguientes requieren entradas con arreglos de esta librería
- rtree: Nos permite acceder a un objeto **rtree** y todas sus funciones para indexación multidimensional
- sklearn.neighbors: Nos permite acceder a un objeto **kdtree** y todas sus funciones para indexación multidimensional

### Realización de algoritmos en base a estructuras

#### Secuencial

En una estructura secuencial, recorremos todo el espacio de elementos de forma lineal de manera que si algún elemento cumple los requerimientos que el algoritmo solicita, este será incluido para su retorno. Se encuentra definido en el proyecto como la clase ```KNN```.

##### KNN search

```py
def _priority_search(self,Q : np.ndarray, D : dict, k : int)
```
Es un método que requiere del espacio de imágenes en forma de vectores y la cantidad *k* de elementos a retornar que más se acerquen al objeto en cuestión. Para facilitar la inserción ordenada, empleamos la librería estandar de python **heapq** de manera que nos permita hacer las funciones básicas **push** a la lista *result* y finalmente seleccionamos aquellos **k** elementos con menor distancia euclidiana.
```py
import heapq

result = []
for id, row in D.items():
    dist = euclidean_distance(Q, row)
    heapq.heappush(result, priority_tuple(id, dist))
return result[:k]
```

Adicionalmente, para permitir que el heap realiza comparaciones con las tuplas ingresadas, se debe crear una clase ```priority_tuple``` que sobrecarga operadores de comparación. De esa manera, los métodos heapq saben como comparar los objetos que almacenan el identificador de la imagen y su respectiva distancia.   

```py
class priority_tuple:
    def __init__(self, _id, _dist) -> None:
        self.id = _id
        self.dist = _dist
    def __lt__(self, ot):
        return self.dist < ot.dist
    def __le__(self, ot):
        return self.dist <= ot.dist
    def __eq__(self, ot):
        return self.dist == ot.dist
    def __ne__(self, ot):
        return self.dist != ot.dist
    def __gt__(self, ot):
        return self.dist > ot.dist
    def __ge__(self, ot):
        return self.dist >= ot.dist
```

##### Range search

```py
def _range_search(self,Q : np.ndarray, D : dict, r : float):
```

Al igual que en KNN search, requerimos de la imagen a consultar, el espacio de imágenes y el radio máximo que una imagen puede encontrarse distanciada de otra. De manera que no existe un número definido de coincidencias que se retornarán ya que ello depende del radio. 

```py
    result = []
    for id, row in D.items():
        dist = euclidean_distance(Q, row)
        if dist < r:
            result.append((id, dist))
    return result
```

#### RTree

En una estructura RTree, empleamos la estructura de datos que lleva el mismo nombre, la cual tiene la capacidad de permitir facilidad en la manipulación de índices multidimensionales. Recordemos que comparte similaridades con un B-Tree. La clase que define sus algoritmos está denominada como **KNN_Rtree**.

##### KNN search
Para obtener los K elementos más cercanos a la consulta en cuestión, empleamos métodos que provienen de la misma librería que nos permite emplear un Rtree. 
```py
(method) nearest: (coordinates: Any, num_results: int = 1, objects: bool = False) -> (Any | Generator[Any, None, None])
```
Con este método, lo empleamos para crear un método de la clase mencionada anteriormente.

```py
def get(self,Q: np.ndarray,data_encoding : dict, k: int):
    output = []
    keys = list(data_encoding.keys())
    self._build(data_encoding=data_encoding)
    query = tuple(Q)
    for p in self._ind.nearest(query, num_results=k):
        output.append((keys[p], self._ind.bounds[p]))
    return output
```

Recordemos que para que la estructura RTree funcione adecuadamente, es necesario que cree un archivo que almacene el índice creado mediante el espacio de imágenes proveído. Esta información se genera de acuerdo a archivos *.data* y *.index*.
```py
def _build(self, data_encoding : dict):
    if os.path.exists("puntos.data"):
        os.remove("puntos.data")
    if os.path.exists("puntos.index"):
        os.remove("puntos.index")
    prop = rtree.index.Property()
    prop.dimension = 128
    prop.buffering_capacity = 3
    prop.dat_extension = "data"
    prop.idx_extension = "index"
    self._ind = rtree.index.Index("puntos", properties=prop)
    for i, value in enumerate(data_encoding.values()):
        self._ind.insert(i, tuple(value))
```

#### HighD

Para emplear métodos basados en la estructura HighD que eviten la maldición de la dimensionalidad, existen las siguientes aplicaciones:
- PCA
- KDTree
- LSH
- Faiss

Para esta ocasión, hemos empleado un KDTree, cuyos métodos y procedimientos son proveídos por la libería **sklearn** en el sub-módulo **neighbors**. Con esto en cuenta, diseñamos un método para la clase denominada KD_Tree que representa la asimilación de KNN-HighD.

##### KNN search

La clase KDTree de sklearn permite realizar consultas KNN mediante el método **query**. Empleamos este método para crear la función que procese consultas KNN.

```py
def get_knn(self,data_encoding : dict, Q: np.ndarray, k, leaf_size=3)
```

- data_encoding: El espacio de imágenes expresado como una serie de puntos
- Q: La imagenn expresada como un punto a buscar
- k: cantidad de elementos similares a retornar
- leaf_size: Cantidad de puntos que el KDTree almacenará por hoja

```py
output = []
keys = list(data_encoding.keys())
enconding = list(data_encoding.values())
tree = KDTree(enconding, leaf_size=leaf_size)
q_reshaped = Q.reshape(1,-1)
dist, ind = tree.query(q_reshaped, k)
for indexes in ind[0]:
    output.append(keys[indexes])
return output
```

##### Range Search

La clase KDTree de sklearn permite realizar consultas KNN mediante el método **query_radius**. Empleamos este método para crear la función que procese consultas KNN.

```py
def get_radius(self,data_encoding : dict, Q: np.ndarray, r, leaf_size=3)
```

- data_encoding: El espacio de imágenes expresado como una serie de puntos
- Q: La imagenn expresada como un punto a buscar
- r: tamaño de la distancia máxima para hallar similaridades
- leaf_size: Cantidad de puntos que el KDTree almacenará por hoja

```py
output = []
keys = list(data_encoding.keys())
enconding = list(data_encoding.values())
tree = KDTree(enconding, leaf_size=leaf_size)
q_reshaped = Q.reshape(1,-1)
ind = tree.query_radius(q_reshaped, r)
for indexes in ind[0]:
    output.append(keys[indexes])
return output
```


## Maldición de dimensionalidad

### Análisis



### Mitigación

## Experimentación

### Tabla de resultados (K=8)

|         | KNN-Secuencial | KNN-Rtree | KNN-HighD |
|---------|----------------|-----------|-----------|
| N=100   |                |           |           |
| N=200   |                |           |           |
| N=400   |                |           |           |
| N=800   |                |           |           |
| N=1600  |                |           |           |
| N=3200  |                |           |           |
| N=6400  |                |           |           |
| N=12800 |                |           |           |

### Gráfica de resultados

### Comentarios
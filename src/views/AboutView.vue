<template>
  <div class="about">
    <div class="form" enctype="multipart/form-data">
      <div class="form-input">
        <label for="imagen" class="izq">Ingrese imagen</label>
        <input
          type="file"
          key="imagen"
          id="imagenSelected"
          @change="handleUpload($event.target.files)"
        />
        <button v-on:click="deleted()">X</button>
      </div>
      <div class="form-input">
        <label for="priority" class="izq">M&eacute;todo de b&uacute;squeda</label>
        <select name="" id="priority" v-model="datos.metodo" class="der">
          <option v-for="opcion in opciones" :key="opcion.id">
            {{ opcion.name }}
          </option>
        </select>
      </div>
      <div class="form-input" v-if="datos.metodo === 'sequential'">
        <label for="priority" class="izq">Tipo de b&uacute;squeda</label>
        <select name="" id="priority" v-model="datos.type" class="der">
          <option v-for="opcion in opciones" :key="opcion.id">
            {{ opcion.name }}
          </option>
        </select>
      </div>
      <div class="form-input2">
        <input
          type="number"
          key="ratio"
          id="ratio"
          placeholder="ratio"
          v-model="datos.ratio"
        />
      <div class="form-input2">
        <input
          type="number"
          key="cantidad"
          id="cantidad"
          placeholder="cantidad de resultados"
          v-model="datos.cantidad"
        />
      </div>
      <div class="form-input2">
        <button class="buscar" v-on:click="issubmited()">Buscar</button>
      </div>
    </div>
    <div v-if="submited === true && success === false">
      <p>Searching ...</p>
    </div>
    <div class="contenido">
    <div v-if="success === true">
      <div v-for="imagen in imagenes" :key="imagen.id">
        <img
          :src="require(`../../backend/lwd/${imagen.carpeta}/${imagen.cont}`)"
        />
        <p>{{ imagen.carpeta }}</p>
      </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      submited: false,
      success: false,
      metodo: null,
      datos: {
        image: new Image(),
        type: "range",
        cantidad: null,
        ratio: null,
      },
      imagenes: [],
      opciones: [
        { name: "sequential", id: 1 },
        { name: "knn-highd", id: 2 },
        { name: "knn-rtree", id: 3 },
      ],
      tipos: [
        { name: "range", id: 1 },
        { name: "priority", id: 2 },
      ]
    };
  },
  methods: {
    deleted() {
      this.datos.image = null;
      document.getElementById("imagenSelected").value = null;
    },
    issubmited() {
      this.submited = true;
      let formData = new FormData();
      formData.append("type", this.datos.type);
      formData.append("img_filename", this.datos.image);
      formData.append("cantidad", this.datos.cantidad);
      formData.append("ratio", this.datos.ratio);
      fetch("</" + this.datos.metodo + "/data?=formData>", {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Content-Type": "multipart/form-data",
        },
      }).then(
        function (response) {
          if (response.status != 200) {
            this.fetchError = response.status;
          } else {
            response.json().then(
              function (data) {
                for(let img of data){
                  let route = "";
                  let imagen_={};
                  let aux = img.name.split("_");
                  route = aux[0] + "_" + aux[1];
                  imagen_["carpeta"] = route;
                  imagen_["cont"] = img.name;
                  this.imagenes.push(imagen_);
                }
              }.bind(this)
            );
          }
        }.bind(this)
      );
    },
    handleUpload(files) {
      this.datos.image = files[0];
    },
  },
};
</script>
<style scoped>
.about {
  display: flex;
  justify-content: center;
  align-items: center;
}
.form {
  background-color: rgb(0, 228, 161);
  width: 90%;
  height: 100px;
  line-height: 6px;
  align-items: center;
  justify-content: center;
  border-radius: 20px;
  display: flex;
  flex-direction: row;
}
.form-input {
  background-color: rgba(170, 223, 254, 0.6);
  margin-left: 1%;
  margin-right: 1%;
  width: 34%;
  border-radius: 15px;
}
.form-input2 {
  background-color: rgba(170, 223, 254, 0.6);
  margin-left: 2%;
  margin-right: 2%;
  width: 10%;
  border-radius: 15px;
}
select {
  background-color: rgb(225, 228, 124);
  border-radius: 20px;
}
.izq {
  margin-right: 1%;
}
.der {
  margin-left: 24%;
}
.buscar {
  background: none;
  border: none;
  width: 100%;
  border-radius: 20px;
}
.buscar:hover {
  background-color: #aadffecc;
  border-radius: 20px;
}
.buscar:focus {
  background-color: rgb(99, 172, 214);
  border-radius: 20px;
}
input[type="number"] {
  border-radius: 20px;
  background-color: rgb(225, 228, 124);
}
</style>

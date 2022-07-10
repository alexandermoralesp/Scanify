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
        <label for="priority" class="izq"
          >M&eacute;todo de b&uacute;squeda</label
        >
        <select
          name=""
          id="priority"
          v-model="datos.metodo"
          class="der"
          @change="opcion()"
        >
          <option v-for="opcion in opciones" :key="opcion.id">
            {{ opcion.name }}
          </option>
        </select>
      </div>
      <div class="form-input" v-if="datos.metodo === 'sequential'">
        <label for="type" class="izq">Tipo de b&uacute;squeda</label>
        <select name="" id="type" v-model="datos.type" class="der">
          <option v-for="opcion in tipos" :key="opcion.id">
            {{ opcion.name }}
          </option>
        </select>
      </div>
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
    <div v-if="success === true">
      <div v-for="imagen in imagenes" :key="imagen.id">
        <img
          :src="require(`@/assets/images/${imagen.id + imagen.extension}`)"
        />
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
        ratio: null,
        type: "range",
        cantidad: null,
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
      ],
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
      formData.append("img_filname", this.datos.image);
      formData.append("cantidad", this.datos.cantidad);
      formData.append("ratio", this.datos.ratio);
      fetch("</" + this.metodo + ">", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "multipart/form-data",
        },
        body: formData,
      }).then(
        function (response) {
          if (response.status != 200) {
            this.fetchError = response.status;
            this.submited = null;
          } else {
            response.json().then(
              function (data) {
                for (let img of data){
                  let cont = 0;
                  let route = '';
                  let imagen_ = {};
                  for(let car of img){
                    if (car != '_'){
                      route += car;
                    }
                    else{
                      if(cont == 0){
                        cont ++;
                      }
                      else {
                        imagen_["carpeta"] = route;
                        imagen_["cont"] = img;
                        this.imagenes.append(imagen_);
                        break;
                      }
                    }
                  }
                }
                this.success = true;
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
  margin-left: 2%;
  margin-right: 2%;
  width: 30%;
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

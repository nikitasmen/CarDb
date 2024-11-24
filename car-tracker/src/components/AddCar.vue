<template>
  <div>
    <h2>Add Car</h2>
    <form @submit.prevent="addCar">
      <div v-for="field in fields" :key="field.name">
        <label :for="field.name">{{ field.label }}</label>
        <input v-model="car[field.name]" :id="field.name" required />
      </div>
      <button type="submit">Add Car</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fields: [
        { name: "modelName", label: "Model Name" },
        { name: "manufacturer", label: "Manufacturer" },
        { name: "year", label: "Year" },
        { name: "originCountry", label: "Origin Country" },
        { name: "category", label: "Category" },
        { name: "modelManufact", label: "Model Manufacturer" },
        { name: "more", label: "More Info (URL)" },
      ],
      car: {
        modelName: "",
        manufacturer: "",
        year: "",
        originCountry: "",
        category: "",
        modelManufact: "",
        more: "",
      },
    };
  },
  methods: {
    async addCar() {
      const response = await fetch("../data/cars.json");
      const cars = await response.json();
      cars.push(this.car);

      // Save new data (requires hosting or API proxy for file writing)
      console.log("Updated Cars:", cars);
    },
  },
};
</script>

<style>
/* Add your styles here */
</style>

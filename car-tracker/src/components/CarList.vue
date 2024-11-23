<template>
  <div>
    <h2>Car List</h2>
    <input v-model="searchQuery" placeholder="Search by Model Name" />
    <table>
      <thead>
        <tr>
          <th>Model Name</th>
          <th>Manufacturer</th>
          <th>Year</th>
          <th>Origin</th>
          <th>Category</th>
          <th>More Info</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="car in filteredCars" :key="car.modelName">
          <td>{{ car.modelName }}</td>
          <td>{{ car.manufacturer }}</td>
          <td>{{ car.year }}</td>
          <td>{{ car.originCountry }}</td>
          <td>{{ car.category }}</td>
          <td>
            <a :href="car.more" target="_blank">View More</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      cars: [],
    };
  },
  computed: {
    filteredCars() {
      return this.cars.filter((car) =>
        car.modelName.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  async created() {
    const response = await fetch("/data/cars.json");
    this.cars = await response.json();
  },
};
</script>

<style>
/* Add your styles here */
</style>

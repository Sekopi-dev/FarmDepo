/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './myApp/templates/**/*.html',
      './static/**/*.js', 
      './node_modules/flowbite/**/*.js',

  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),
    
  ],
}


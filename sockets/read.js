const readline = require('readline');

// Crea una interfaz para leer desde la entrada estándar
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// Pregunta al usuario
rl.question('Por favor ingresa algo: ', (input) => {
  // El usuario ha ingresado algo, puedes procesar su entrada aquí
  console.log(`Ingresaste: ${input}`);

  // Cierra la interfaz
  rl.close();
});

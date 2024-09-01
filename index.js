// // resisar este issues para ver si hay solucion de inicio de session
// // https://github.com/pedroslopez/whatsapp-web.js/pull/2816



const { exec } = require('child_process');
const fs = require('fs');
const qrcode = require('qrcode-terminal');
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const path = require('path');

// Ruta al directorio que contiene el archivo HTML
const directorio = '.wwebjs_cache';

// Función que retorna una promesa que se resuelve con un valor booleano
function comprobarArchivoHtml() {
    return new Promise((resolve, reject) => {
        fs.readdir(directorio, (err, archivos) => {
            if (err) {
                reject('Error al leer el directorio:', err);
                return;
            }

            // Filtrar los archivos HTML
            const archivosHtml = archivos.filter(archivo => path.extname(archivo) === '.html');

            // Comprobar si hay exactamente un archivo HTML
            if (archivosHtml.length === 1) {
                resolve(true);
            } else {
                resolve(false);
            }
        });
    });
}

// Inicializar el cliente de WhatsApp solo si el archivo HTML está presente
comprobarArchivoHtml()
    .then(existeUnArchivoHtml => {
        if (existeUnArchivoHtml) {
            console.log('Bot Iniciando');

            const client = new Client({
                authStrategy: new LocalAuth({
                    // session: sessionData, // Asume que sessionData está correctamente configurado
                    puppeteer: {
                        args: ['--no-sandbox', '--disable-setuid-sandbox']
                    }
                })
            });

            // Aviso si el bot está listo
            client.on('ready', () => {
                console.log('Bot en escuha de comandos:');
            });

            // Comandos del bot
            client.on('message', async message => {

                const contact = await message.getContact();
                const contactName = contact.pushname || contact.notifyName || 'Undefined';
                console.log('');
                console.log(`by: ${contactName}`);
                console.log('Command:',message.body);

                const partes = message.body.split(' ');
    
                // Verificar si el comando /s tiene al menos dos partes y el argumento no está vacío
                if (partes.length < 2 || partes[1].trim() === '') {
                    // Manejar el caso en que no se proporciona el argumento
                    message.reply(`Respuesta: command ${partes[0]} requiere suministro`);
                    console.error(`ReponsePython: command ${partes[0]} requiere suministro`);
                    return;
                }
                

                if (message.body.startsWith('/s ')) {
                    const numero = message.body.split(' ')[1];
                    
                    exec(`python3.7 C:\\Users\\nimun\\Documents\\Js\\Bot\\py\\Utils.py ${numero} --mode apiUrl`, (error, stdout, stderr) => {
                        if (error) {
                            console.error(`Error ejecutando el script: ${error.message}`);
                            return;
                        }
                        if (stderr) {
                            console.error(`Error estándar: ${stderr}`);
                            return;
                        }
                        message.reply(`Respuesta: ${stdout}`);
                        console.log(`ReponsePython: ${stdout}`);
                    });
                }

                if (message.body.startsWith('/d ')) {
                    const numero = message.body.split(' ')[1];
                    exec(`python3.7 C:\\Users\\nimun\\Documents\\Js\\Bot\\py\\Utils.py ${numero} --mode apiDoc`, (error, stdout, stderr) => {
                        if (error) {
                            console.error(`Error ejecutando el script: ${error.message}`);
                            return;
                        }
                        if (stderr) {
                            console.error(`Error estándar: ${stderr}`);
                            return;
                        }

                        if (stdout.trim() === 'False') {
                            message.reply(`Suministro No Existe`);

                        } else {
                            if (stdout.trim().endsWith('.pdf')){
                            const pdf = MessageMedia.fromFilePath(`${__dirname}/py/pdf/${numero}.pdf`);
                            message.reply(`Respuesta: ${stdout.trim()}`, undefined, { media: pdf, quotedMessageId: message.id._serialized });
                            }

                            else{
                                message.reply(`Respuesta: ${stdout.trim()}`);
                            };
                        }
                        console.log(`ReponsePython: ${stdout}`);
                    });
                }
            });

            client.initialize();

        } else {
            console.log('No se encontró ningún archivo HTML. Por favor, escanee el QR nuevamente.');

            const client = new Client({
                authStrategy: new LocalAuth({
                    puppeteer: {
                        args: ['--no-sandbox', '--disable-setuid-sandbox']
                    }
                })
            });

            // Manejar el evento QR generado
            client.on('qr', qr => {
                qrcode.generate(qr, { small: true });
            });

            client.initialize();
        }
    })
    .catch(error => {
        console.error('Session caducada escanerar qr:');
        const client = new Client({
            authStrategy: new LocalAuth({
                puppeteer: {
                    args: ['--no-sandbox', '--disable-setuid-sandbox']
                }
            })
        });

        // Manejar el evento QR generado
        client.on('qr', qr => {
            qrcode.generate(qr, { small: true });
        });

        client.on('ready', () => {
            console.log('Session iniciada detener y iniciar el app.js');
        });

        client.initialize();
    });


// const { Client,LocalAuth,MessageMedia } = require('whatsapp-web.js');
// const qrcode = require('qrcode-terminal');
// const fs = require('fs');
// const path = require('path');

// // Crea una nueva instancia del cliente de WhatsApp
// const client = new Client({
//     authStrategy: new LocalAuth({
//         // session: sessionData,
//         puppeteer:{
//             args:['--no-sandbox','--disable-setuid-sandbox']
//         }

//     })
// });

// Genera y muestra el código QR para la autenticación
// client.on('qr', qr => {
//     qrcode.generate(qr, { small: true });
// });

// Maneja el evento de autenticación exitoso
// client.on('authenticated', () => {
//     console.log('Autenticado correctamente');
// });

// client.on('ready', () => {
//     console.log('Cliente listo');
// });

// // Maneja el evento cuando se recibe un mensaje
// client.on('message', message => {
//     // Obtiene el nombre del remitente
//     message.getContact().then(contact => {
//         console.log(`Mensaje recibido de: ${contact.pushname || contact.notifyName}`);
//     });
// });

// // Inicia el cliente
// client.initialize();

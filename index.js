// const { exec } = require('child_process');

// exec('python3.7 C:\\Users\\nimun\\Documents\\Js\\Bot\\py\\main.py 1337535', (error, stdout, stderr) => {
//     if (error) {
//         console.error(`Error ejecutando el script: ${error.message}`);
//         return;
//     }
//     if (stderr) {
//         console.error(`Error estándar: ${stderr}`);
//         return;
//     }
//     console.log(`Salida estándar: ${stdout}`);
// });


const { exec } = require('child_process');
const fs = require('fs');
const qrcode = require('qrcode-terminal');
const { measureMemory } = require('vm');
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');


// exec('python3.7 main.py 1337566');

// Intenta cargar la sesión desde un archivo JSON

let sessionData;
if (fs.existsSync('./session.json')) {
    sessionData = require('./session.json');
}

const client = new Client({
    authStrategy: new LocalAuth({
        session: sessionData
    })
});

// codigo que guarda la seccion de whatsapp

// client.on('qr', qr => {
//     qrcode.generate(qr, { small: true });
// });

// client.on('authenticated', (session) => {
//     console.log('Autenticado con éxito');

//     // Guarda la sesión en un archivo JSON
//     fs.writeFile('./session.json', JSON.stringify(session), (err) => {
//         if (err) {
//             console.error('Error al guardar la sesión', err);
//         } else {
//             console.log('Sesión guardada con éxito');
//         }
//     });
// });


client.on('ready', () => {
    console.log('Cliente listo');
});

// Escuchar mensajes
// client.on('message', message => {
//     console.log(`Mensaje recibido: ${message.body}`);
    
//     // Responder al mensaje
//     if (message.body === 'Hola') {
//         message.reply('¡Hola! ¿Cómo estás?');

//     } else if (message.body.startsWith('/s ')) {
//         const numero = message.body.split(' ')[1];
//         if (!isNaN(numero)){
//             exec('python3.7 C:\Users\nimun\Documents\Js\Bot\py\main.py ${numero}',(error, stdout, stderr) => {
//                 if (error) {
//                     message.reply(`Error al ejecutar el script: ${error.message}`);
//                     return;
//                 }
//                 if (stderr) {
//                     message.reply(`Error en el script: ${stderr}`);
//                     return;
//                 }
//             });

//             // El nombre del archivo se imprime por el script Python, capturamos esto
//             const filename = stdout.trim(); // Suponiendo que stdout solo contiene el nombre del archivo

//             if (fs.existsSync(filename)){
//                 client.sendMessage(message.from,{
//                     caption: 'Aquí está el archivo solicitado:',
//                     file: fs.readFileSync(filename),
//                     filename: path.basename(filename)
//                 });
//             };
//         };

//     } else if (message.body.includes('adiós')) {
//         message.reply('¡Hasta luego!');

//     } else {
//         message.reply('No entiendo tu mensaje.');
//     }
// });

// const pdf = MessageMedia.fromFilePath(`${__dirname}/py/pdf/`)

// client.on('message', message => {
//     if (message.body.startsWith('/s ')) 
//         {
//             const numero = message.body.split(' ')[1];
//             exec(`python3.7 C:\\Users\\nimun\\Documents\\Js\\Bot\\py\\main.py ${numero}`, (error, stdout, stderr) => {
//                 if (error) {
//                     console.error(`Error ejecutando el script: ${error.message}`);
//                     return;
//                 }
//                 if (stderr) {
//                     console.error(`Error estándar: ${stderr}`);
//                     return;
//                 }

//                     // Define la URL esperada
//                 const expectedUrl = 'https://docs.google.com/gview?url=http://www.easyenvios.com/escan1/006/003/3/00000001/01/00300000001000001.TIF&embedded=true';
                
//                 // Verifica si la salida estándar coincide con la URL esperada
//                 if (stdout.trim() === expectedUrl) {
//                     message.reply(`Suministro No Existe`);
//                 } else {
//                     // Enviar la salida estándar en caso de que no coincida
//                     message.reply(`Salida estándar: ${stdout}`);
//                 }
                
//                 // Opcionalmente, loguea la salida estándar para depuración
//                 console.log(`Salida estándar: ${stdout}`);
                
//                 // const filename = `C:\\Users\\nimun\\Documents\\Js\\Bot\\py\\pdf\\${stdout}`;
//                 // if (fs.existsSync(filename)){
//                 //     const fileData = fs.readFileSync(filename);
//                 //     const media = new MessageMedia('application/pdf', fileData.toString('base64'), path.basename(stderr));

//                 //     client.sendMessage(message.from, media, { caption: 'Aquí está el archivo solicitado:' })
//                 //         .then(() => {
//                 //             console.log('Archivo enviado exitosamente.');
//                 //         })
//                 //         .catch(err => {
//                 //             console.error('Error al enviar el archivo:', err);
//                 //         });
//                 // };

//             });
            
        
//         }
//     if (message.body.startsWith('/d ')) {
//         const numero = message.body.split(' ')[1];
//         const pdf = MessageMedia.fromFilePath(`${__dirname}/py/pdf/${numero}.pdf`)
//         console.log(`Salida estándar: ${pdf}`);
//         client.sendMessage(message.from,pdf)
//         exec(`python3.7 C:\\Users\\nimun\\Documents\\Js\\Bot\\py\\sendpdf.py ${numero}`, (error, stdout, stderr) => {
//             if (error) {
//                 console.error(`Error ejecutando el script: ${error.message}`);
//                 return;
//             }
//             if (stderr) {
//                 console.error(`Error estándar: ${stderr}`);
//                 return;
//             }
            
//             // Verifica si la salida estándar coincide con la URL esperada
//             if (stdout.trim() === 'False') {
//                 message.reply(`Suministro No Existe`);

//             } else {
//                 // Enviar la salida estándar en caso de que no coincida
//                 // message.reply(`Salida estándar: ${stdout}`);
//                 client.sendMessage(message.from,pdf,{caption:'Salida estándar'})
//             }
            
//             // Opcionalmente, loguea la salida estándar para depuración
//             console.log(`Salida estándar: ${stdout}`);

//         });

//     }
    
//     else {};

// });

// client.initialize();

client.on('message',async message => {
    if (message.body.startsWith('/s ')) {
        const numero = message.body.split(' ')[1];
        exec(`python3.7 C:\\Users\\nimun\\Documents\\Js\\Bot\\py\\main.py ${numero}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error ejecutando el script: ${error.message}`);
                return;
            }
            if (stderr) {
                console.error(`Error estándar: ${stderr}`);
                return;
            }

            const expectedUrl = 'https://docs.google.com/gview?url=http://www.easyenvios.com/escan1/006/003/3/00000001/01/00300000001000001.TIF&embedded=true';

            if (stdout.trim() === expectedUrl) {
                message.reply(`Suministro No Existe`);
            } else {
                message.reply(`Salida estándar: ${stdout}`);
            }

            console.log(`Salida estándar: ${stdout}`);
        });
    } 

    if (message.body.startsWith('/d ')) {
        const numero = message.body.split(' ')[1];
        console.log(`Salida estándar: ${numero}`);
        exec(`python3.7 C:\\Users\\nimun\\Documents\\Js\\Bot\\py\\sendpdf.py ${numero}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error ejecutando el script: ${error.message}`);
                return;
            }
            if (stderr) {
                console.error(`Error estándar: ${stderr}`);
                return;
            }
            // });

            if (stdout.trim() === 'False') {
                message.reply(`Suministro No Existe`);

            } else {
                const pdf = MessageMedia.fromFilePath(`${__dirname}/py/pdf/${numero}.pdf`);
                // message.reply(`Salida estándar`,pdf);
                // client.sendMessage(message.from, pdf);
                // message.reply(pdf, undefined, { quotedMessageId: message.id._serialized });
                message.reply('Salida estandar', undefined, { media: pdf, quotedMessageId: message.id._serialized });
            }

            console.log(`Salida estándar: ${stdout}`);
            } 
        );
    }
});

client.initialize();


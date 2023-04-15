const { app, BrowserWindow, ipcMain } = require("electron");
const PDFDocument = require("pdfkit");
const path = require("path");
const fs = require("fs");

function createWindow() {
    let mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        resizable: false,
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
        },
    });

    mainWindow.menuBarVisible = false;
    mainWindow.loadFile(path.join(__dirname, "index.html"));
};

function printPDF(_, pdfFileName) {
    let doc = new PDFDocument();
    let pdfPath = path.join(__dirname, `${pdfFileName}.pdf`);

    doc.pipe(fs.createWriteStream(pdfPath));
    doc.fontSize(12).text("HELLO WORLD!");
    doc.end();

    let pdfWindow = new BrowserWindow({
        width: 800,
        height: 600,
        resizable: false,
    });

    pdfWindow.loadFile(pdfPath);
    pdfWindow.webContents.print({});
}

app.whenReady().then(() => {
    ipcMain.on("print", printPDF); 

    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    })
});

const electron = require('electron');
const express = require('express');

// Module to control application life.
const app = electron.app;
// Module to create native browser window.
const BrowserWindow = electron.BrowserWindow;

const path = require('path');
const url = require('url');

let mainWindow;

const server = require('./backend/server')

function createWindow() {
    // Create the browser window.
    mainWindow = new BrowserWindow({
        height: 563,
        useContentSize: true,
        width: 1000,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true,
            webSecurity: false
        },
    });
    mainWindow.setMenu(null);

    // and load the index.html of the app.

    mainWindow.loadURL(`file://${__dirname}/build/index.html`)

    // Emitted when the window is closed.
    mainWindow.on('closed', function () {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        mainWindow = null
    })
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.

app.on('ready', createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', function () {
    // On OS X it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit()
    }
});

app.on('activate', function () {
    // On OS X it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (mainWindow === null) {
        createWindow()
    }
});

app.on('ligarBot', async (event) => {
    spawn('cd bot && bot.exe');
});

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
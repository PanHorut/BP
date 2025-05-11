/**
 * ================================================================================
 * File: websocket.js
 * Description:
 *       Utility module for handling WebSocket communication with server.
 * Author: Dominik Horut (xhorut01)
 * ================================================================================
 */

let socket = null;

/**
 * Establishes a WebSocket connection and sets up event listeners.
 * 
 * @param {string} url - The WebSocket server URL.
 * @param {function} onMessageReceived - Callback for incoming messages.
 * @param {function} onError - Callback for connection errors.
 * @param {function} onOpen - Callback when connection is successfully opened.
 * @param {function} onClose - Callback when connection is closed.
 */
export const connectWebSocket = (url, onMessageReceived, onError, onOpen, onClose) => {
    socket = new WebSocket(url);

    // Triggered when the connection is opened
    socket.onopen = (event) => {
        console.log("WebSocket connected");
        if (onOpen) onOpen(event);
    };

    // Triggered when a message is received from the server
    socket.onmessage = (event) => {
        console.log("Message received: ", event.data);
        if (onMessageReceived) onMessageReceived(event);
    };

     // Triggered on connection error
    socket.onerror = (error) => {
        console.error("WebSocket error: ", error);
        if (onError) onError(error);
    };

    // Triggered when the connection is closed
    socket.onclose = (event) => {
        console.log("WebSocket disconnected", event);
        if (onClose) onClose(event);
    };
};

/**
 * Gracefully closes the WebSocket connection, if open.
 */
export const disconnectWebSocket = () => {
    if (socket) {
        socket.close();
        socket = null;
    }
};

/**
 * Sends a message through the WebSocket if the connection is open.
 * 
 * @param {string} message - The message string to send.
 */
export const sendMessage = (message) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(message);
    }
};

// websocket.js

let socket = null;

export const connectWebSocket = (url, onMessageReceived, onError, onOpen, onClose) => {
    socket = new WebSocket(url);

    socket.onopen = (event) => {
        console.log("WebSocket connected");
        if (onOpen) onOpen(event);
    };

    socket.onmessage = (event) => {
        console.log("Message received: ", event.data);
        if (onMessageReceived) onMessageReceived(event);
    };

    socket.onerror = (error) => {
        console.error("WebSocket error: ", error);
        if (onError) onError(error);
    };

    socket.onclose = (event) => {
        console.log("WebSocket disconnected", event);
        if (onClose) onClose(event);
    };
};

export const disconnectWebSocket = () => {
    if (socket) {
        socket.close();
        socket = null;
    }
};

export const sendMessage = (message) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(message);
    }
};

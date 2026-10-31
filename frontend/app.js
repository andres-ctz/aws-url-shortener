
const API_URL = "http://54.160.217.117";

// Elementos HTML
const form = document.getElementById("shorten-form");
const originalUrlInput = document.getElementById("original-url");
const shortenButton = document.getElementById("shorten-button");

const message = document.getElementById("message");
const result = document.getElementById("result");

const shortUrlElement = document.getElementById("short-url");
const originalLinkElement = document.getElementById("original-link");
const copyButton = document.getElementById("copy-button");


// Crear un enlace corto
form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const originalUrl = originalUrlInput.value.trim();

    message.textContent = "";
    result.classList.add("hidden");

    shortenButton.disabled = true;
    shortenButton.textContent = "Generando enlace...";

    try {
        const response = await fetch(`${API_URL}/shorten`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                original_url: originalUrl
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "No se pudo generar el enlace."
            );
        }

        // Mostrar el enlace corto
        shortUrlElement.textContent = data.short_url;
        shortUrlElement.href = data.short_url;

        // Mostrar la URL original
        originalLinkElement.textContent = data.original_url;
        originalLinkElement.href = data.original_url;

        result.classList.remove("hidden");

        message.textContent = "¡Enlace creado correctamente!";
        message.style.color = "#4ade80";

        form.reset();

    } catch (error) {
        message.textContent = error.message;
        message.style.color = "#f87171";

    } finally {
        shortenButton.disabled = false;
        shortenButton.textContent = "Acortar enlace";
    }
});


// Copiar el enlace corto
copyButton.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(shortUrlElement.href);

        copyButton.textContent = "¡Copiado!";

        setTimeout(() => {
            copyButton.textContent = "Copiar";
        }, 2000);

    } catch (error) {
        message.textContent = "No se pudo copiar el enlace.";
        message.style.color = "#f87171";
    }
});

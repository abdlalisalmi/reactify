document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("bubble-container");
  const sendMessageBtn = document.getElementById("send-message");
  const messageTextInput = document.getElementById("msg-input");
  const reactionButtons = document.querySelectorAll(".reaction-btn");
  const authModalBtn = document.getElementById("openModalBtn");
  const qrCodes = document.querySelectorAll(".qr-code");
  const inputContainer = document.getElementById("input-container");

  //   display message
  var messages = JSON.parse(document.getElementById("messages").textContent);
  let index = 0;

  const interval = setInterval(() => {
    if (index < messages.length) {
      const msg = messages[index];
      const sanitizedContent = DOMPurify.sanitize(msg.content);
      createBubble(msg.full_name, sanitizedContent);
      index++;
    } else {
      index = 0; // Reset index to loop through messages again
    }
  }, 2000); // every 2 seconds

  var fullName = localStorage.getItem("fullName") || "Anonymous";

  const roomId = JSON.parse(document.getElementById("room-id").textContent);
  const WS_PROTOCOL =
    window.location.protocol === "https:" ? "wss://" : "ws://";

  const chatSocket = new WebSocket(
    WS_PROTOCOL + window.location.host + "/ws/chat/" + roomId + "/"
  );

  chatSocket.onopen = function (e) {
    console.log("Chat Connected");
  };

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    createBubble(data.full_name, data.message, null, true);
  };

  chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };

  function sendMessage(text) {
    const textTrimed = messageTextInput.value.trim().slice(0, 50);
    messages.push({ full_name: fullName, content: textTrimed });
    chatSocket.send(
      JSON.stringify({
        message: textTrimed,
        full_name: fullName,
      })
    );
  }

  function handleAuth() {
    if (!fullName || fullName === "Anonymous") {
      authModalBtn.style.display = "block";
      inputContainer.style.display = "none";
      qrCodes.forEach((qrCode) => {
        qrCode.style.display = "block";
      });
    } else {
      inputContainer.style.display = "block";
      authModalBtn.style.display = "none";
      qrCodes.forEach((qrCode) => {
        qrCode.style.display = "none";
      });
    }
  }
  handleAuth();

  // Array of colors for custom text bubbles
  const bubbleColors = [
    { bg: "bg-blue-100", text: "text-blue-600" },
    { bg: "bg-green-100", text: "text-green-600" },
    { bg: "bg-purple-100", text: "text-purple-600" },
    { bg: "bg-pink-100", text: "text-pink-600" },
    { bg: "bg-yellow-100", text: "text-yellow-600" },
    { bg: "bg-indigo-100", text: "text-indigo-600" },
    { bg: "bg-teal-100", text: "text-teal-600" },
  ];

  // Reaction colors mapping
  const reactionColors = {
    "❤️": { bg: "bg-red-100", text: "text-red-600" },
    "👍": { bg: "bg-blue-100", text: "text-blue-600" },
    "😄": { bg: "bg-yellow-100", text: "text-yellow-600" },
    "😮": { bg: "bg-green-100", text: "text-green-600" },
    "🔥": { bg: "bg-orange-100", text: "text-orange-600" },
    "🎉": { bg: "bg-pink-100", text: "text-pink-600" },
  };

  function createBubble(username, text, clickPosition = null, system = false) {
    const bubble = document.createElement("div");
    const container = document.getElementById("bubble-container"); // Assuming container is defined elsewhere

    // Reactions list
    const reactions = ["❤️", "👍", "😄", "😮", "🔥", "🎉", "#Congratulations"];
    const isReaction = reactions.includes(text);

    // Size between 60px and 120px for reactions, or fixed size for messages
    const size = isReaction ? Math.floor(Math.random() * 60) + 60 : 120;

    // Position
    const maxX = container.clientWidth - size;
    let posX;

    if (clickPosition) {
      // If created from container click, use that position
      posX = clickPosition.x - size / 2;
    } else {
      // Random position
      posX = Math.floor(Math.random() * maxX);
    }

    // Colors based on text or random
    let bgColor, textColor;
    if (reactionColors[text]) {
      bgColor = reactionColors[text].bg;
      textColor = reactionColors[text].text;
    } else {
      const randomColor =
        bubbleColors[Math.floor(Math.random() * bubbleColors.length)];
      bgColor = randomColor.bg;
      textColor = randomColor.text;
    }

    // Add floating animation class
    const floatClass = Math.random() > 0.5 ? "float-left" : "float-right";

    bubble.style.position = "absolute";
    bubble.style.left = `${posX}px`;
    bubble.style.bottom = `${
      clickPosition
        ? container.clientHeight - clickPosition.y - size / 2
        : -size
    }px`;

    const sanitizedContent = DOMPurify.sanitize(text);
    // First add text content
    if (isReaction) {
      bubble.innerHTML = `<div class="bubble flex justify-center items-center w-16 h-16 rounded-full text-xl ${bgColor} ${textColor} ${floatClass}">
      ${sanitizedContent}
    </div>`;
    } else if (text.startsWith("#")) {
      bubble.innerHTML = `<div class="bubble flex justify-center items-center rounded-xl px-3 py-1 text-sm ${bgColor} ${textColor} ${floatClass}">
      ${sanitizedContent}
    </div>`;
    } else {
      // For regular messages
      bubble.innerHTML = `<div class="bubble bg-white rounded-full py-3 px-4 flex items-center shadow-sm max-w-lg ${floatClass}">
      <!-- Avatar -->
      <div class="bg-violet-500 rounded-full w-10 h-10 flex items-center justify-center mr-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      </div>
      <!-- User Info -->
      <div class="flex flex-col">
      <span class="font-semibold text-md text-gray-900">${username}</span>
      <span class="text-gray-500 text-sm">${sanitizedContent}</span>
      </div>
    </div>`;
    }

    // Add bubble to container
    container.appendChild(bubble);

    // Calculate speed based on window size
    // Taller windows get faster animations to maintain reasonable animation time
    const baseSpeed = 1.5;
    const containerHeight = container.clientHeight;
    const speedFactor = containerHeight / 800; // Normalize based on 800px reference height
    let speed = baseSpeed * speedFactor * (Math.random() * 0.5 + 0.75); // Add some randomness but keep within reasonable range

    // Starting position
    let currentY = clickPosition
      ? container.clientHeight - clickPosition.y - size / 2
      : -size;

    // Animation ID for cleanup
    let animationId;

    // Track time for smoother animation
    let lastTimestamp = null;

    // Animation function using requestAnimationFrame with timestamp
    function animateBubble(timestamp) {
      if (!lastTimestamp) {
        lastTimestamp = timestamp;
      }

      // Calculate time delta for smooth animation regardless of frame rate
      const delta = (timestamp - lastTimestamp) / 16.67; // Normalize to 60fps
      lastTimestamp = timestamp;

      // Move based on speed, time delta and window height
      currentY += speed * delta;
      bubble.style.bottom = `${currentY}px`;

      // Remove bubble when it goes off the top
      if (currentY >= containerHeight + size) {
        bubble.remove();
        return;
      }

      // Continue animation
      animationId = requestAnimationFrame(animateBubble);
    }

    // Start animation
    animationId = requestAnimationFrame(animateBubble);

    // Click event to remove bubble
    bubble.addEventListener("click", (event) => {
      event.stopPropagation();
      bubble.classList.add("pop");

      // Cancel the animation to prevent memory leaks
      if (animationId) {
        cancelAnimationFrame(animationId);
      }

      setTimeout(() => bubble.remove(), 400);
    });

    // Handle window resize - adjust speed for new container height
    const handleResize = () => {
      let newContainerHeight = container.clientHeight;
      let newSpeedFactor = newContainerHeight / 800;
      // Update speed based on new container height
      speed = baseSpeed * newSpeedFactor * (Math.random() * 0.5 + 0.75);
    };

    // Add resize listener
    window.addEventListener("resize", handleResize);

    // Return a cleanup function to be called if needed
    return () => {
      if (animationId) {
        cancelAnimationFrame(animationId);
      }
      window.removeEventListener("resize", handleResize);
      if (bubble.parentNode) {
        bubble.remove();
      }
    };
  }

  // Add bubble when button is clicked
  if (sendMessageBtn) {
    sendMessageBtn.addEventListener("click", () => {
      const customText = messageTextInput.value.trim();
      if (customText) {
        sendMessage(customText);

        messageTextInput.value = ""; // Clear input after adding
      }
      messageTextInput.focus();
    });
  }

  // Add bubble when Enter key is pressed in the input
  if (messageTextInput) {
    messageTextInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        const customText = messageTextInput.value.trim();
        if (customText) {
          sendMessage(customText);
          messageTextInput.value = ""; // Clear input after adding
        }
      }
    });
  }

  // Add reaction bubbles when reaction buttons are clicked
  if (reactionButtons) {
    reactionButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const reaction = button.getAttribute("data-reaction");
        createBubble("", reaction);

        // Button press effect
        button.classList.add("scale-95");
        setTimeout(() => {
          button.classList.remove("scale-95");
        }, 100);
      });
    });
  }

  // Automatically create bubbles periodically
  function startAutoBubbles() {
    // Create 1-3 bubbles initially
    for (let i = 0; i < Math.floor(Math.random() * 3) + 1; i++) {
      setTimeout(() => {
        const reactions = Array.from(reactionButtons).map((btn) =>
          btn.getAttribute("data-reaction")
        );
        const randomReaction =
          reactions[Math.floor(Math.random() * reactions.length)];
        createBubble("", randomReaction, null, true);
      }, Math.random() * 500);
    }

    // Create new bubbles periodically
    setInterval(() => {
      if (Math.random() > 0.6) {
        // 40% chance to create a bubble
        const reactions = Array.from(reactionButtons).map((btn) =>
          btn.getAttribute("data-reaction")
        );
        const randomReaction =
          reactions[Math.floor(Math.random() * reactions.length)];
        createBubble("", randomReaction, null, true);
      }
    }, 500);
  }

  // Start automatic bubble creation
  startAutoBubbles();

  // Focus the input field on page load
  if (messageTextInput) {
    messageTextInput.focus();
  }

  // Handle non-autenticated users
});

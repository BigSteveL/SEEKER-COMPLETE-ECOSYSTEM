/**
 * SEEKER Video Conference Module
 * Real-time video conferencing with WebRTC integration
 */

class SEEKERVideoConference {
    constructor() {
        this.localStream = null;
        this.peerConnections = {};
        this.localVideo = null;
        this.isVideoActive = false;
        this.conferenceId = null;
        this.participants = [];
        
        this.init();
    }
    
    init() {
        console.log('📹 Initializing SEEKER Video Conference...');
        this.initializeEventListeners();
        console.log('✅ Video Conference initialized');
    }
    
    initializeEventListeners() {
        console.log('🔗 Adding video conference event listeners...');
        
        // Wait a bit for DOM to be ready
        setTimeout(() => {
            // Conference creation and joining
            const createConferenceBtn = document.getElementById('createConferenceBtn');
            const joinConferenceBtn = document.getElementById('joinConferenceBtn');
            
            console.log('🔍 Found createConferenceBtn:', !!createConferenceBtn);
            console.log('🔍 Found joinConferenceBtn:', !!joinConferenceBtn);
            
            if (createConferenceBtn) {
                createConferenceBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('🎬 Create conference clicked');
                    this.createConference();
                });
                console.log('✅ Create conference button listener added');
            } else {
                console.error('❌ Create conference button not found');
            }
            
            if (joinConferenceBtn) {
                joinConferenceBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('🚪 Join conference clicked');
                    this.joinConference();
                });
                console.log('✅ Join conference button listener added');
            } else {
                console.error('❌ Join conference button not found');
            }
            
            // Video controls
            const startVideoBtn = document.getElementById('startVideoBtn');
            const stopVideoBtn = document.getElementById('stopVideoBtn');
            
            console.log('🔍 Found startVideoBtn:', !!startVideoBtn);
            console.log('🔍 Found stopVideoBtn:', !!stopVideoBtn);
            
            if (startVideoBtn) {
                startVideoBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('▶️ Start video clicked');
                    this.startVideo();
                });
                console.log('✅ Start video button listener added');
            } else {
                console.error('❌ Start video button not found');
            }
            
            if (stopVideoBtn) {
                stopVideoBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('⏹️ Stop video clicked');
                    this.stopVideo();
                });
                console.log('✅ Stop video button listener added');
            } else {
                console.error('❌ Stop video button not found');
            }
            
            // Chat functionality
            const sendChatBtn = document.getElementById('sendChatBtn');
            const chatInput = document.getElementById('chat-input');
            
            if (sendChatBtn) {
                sendChatBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    console.log('💬 Send chat clicked');
                    this.sendChatMessage();
                });
                console.log('✅ Send chat button listener added');
            }
            
            if (chatInput) {
                chatInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        console.log('💬 Chat enter pressed');
                        this.sendChatMessage();
                    }
                });
                console.log('✅ Chat input listener added');
            }
            
            console.log('✅ All video conference event listeners initialized');
        }, 100); // Wait 100ms for DOM to be ready
    }
    
    async createConference() {
        try {
            console.log('🎬 Creating conference...');
            
            // Generate conference ID
            this.conferenceId = this.generateConferenceId();
            
            // Update UI
            const titleInput = document.getElementById('conference-title');
            if (titleInput) {
                titleInput.value = `SEEKER Conference - ${this.conferenceId}`;
            }
            
            // Add system message
            this.addChatMessage('System', `Conference created: ${this.conferenceId}`, 'system');
            
            // Initialize video if available
            await this.initializeVideo();
            
            console.log('✅ Conference created:', this.conferenceId);
            
        } catch (error) {
            console.error('❌ Failed to create conference:', error);
            this.addChatMessage('System', 'Failed to create conference', 'error');
        }
    }
    
    async joinConference() {
        try {
            console.log('🚪 Joining conference...');
            
            const titleInput = document.getElementById('conference-title');
            const participantInput = document.getElementById('participant-name');
            
            if (!titleInput || !titleInput.value) {
                this.addChatMessage('System', 'Please enter a conference title', 'warning');
                return;
            }
            
            if (!participantInput || !participantInput.value) {
                this.addChatMessage('System', 'Please enter your name', 'warning');
                return;
            }
            
            // Update conference ID
            this.conferenceId = titleInput.value;
            
            // Add system message
            this.addChatMessage('System', `${participantInput.value} joined the conference`, 'system');
            
            // Initialize video if available
            await this.initializeVideo();
            
            console.log('✅ Joined conference:', this.conferenceId);
            
        } catch (error) {
            console.error('❌ Failed to join conference:', error);
            this.addChatMessage('System', 'Failed to join conference', 'error');
        }
    }
    
    async startVideo() {
        try {
            console.log('▶️ Starting video...');
            
            if (this.isVideoActive) {
                console.log('⚠️ Video already active');
                return;
            }
            
            // Get user media
            this.localStream = await navigator.mediaDevices.getUserMedia({
                video: true,
                audio: true
            });
            
            // Display local video
            this.localVideo = document.getElementById('localVideo');
            if (this.localVideo) {
                this.localVideo.srcObject = this.localStream;
                this.localVideo.play();
            }
            
            this.isVideoActive = true;
            
            // Update UI
            const startBtn = document.getElementById('startVideoBtn');
            const stopBtn = document.getElementById('stopVideoBtn');
            
            if (startBtn) startBtn.disabled = true;
            if (stopBtn) stopBtn.disabled = false;
            
            this.addChatMessage('System', 'Video started', 'system');
            console.log('✅ Video started successfully');
            
        } catch (error) {
            console.error('❌ Failed to start video:', error);
            this.addChatMessage('System', 'Failed to start video: ' + error.message, 'error');
        }
    }
    
    stopVideo() {
        try {
            console.log('⏹️ Stopping video...');
            
            if (!this.isVideoActive) {
                console.log('⚠️ Video not active');
                return;
            }
            
            // Stop all tracks
            if (this.localStream) {
                this.localStream.getTracks().forEach(track => {
                    track.stop();
                });
                this.localStream = null;
            }
            
            // Clear video display
            if (this.localVideo) {
                this.localVideo.srcObject = null;
            }
            
            this.isVideoActive = false;
            
            // Update UI
            const startBtn = document.getElementById('startVideoBtn');
            const stopBtn = document.getElementById('stopVideoBtn');
            
            if (startBtn) startBtn.disabled = false;
            if (stopBtn) stopBtn.disabled = true;
            
            this.addChatMessage('System', 'Video stopped', 'system');
            console.log('✅ Video stopped successfully');
            
        } catch (error) {
            console.error('❌ Failed to stop video:', error);
            this.addChatMessage('System', 'Failed to stop video: ' + error.message, 'error');
        }
    }
    
    async initializeVideo() {
        try {
            console.log('📹 Initializing video...');
            
            // Check if video is already initialized
            if (this.localVideo) {
                console.log('✅ Video already initialized');
                return;
            }
            
            // Get video element
            this.localVideo = document.getElementById('localVideo');
            if (!this.localVideo) {
                console.error('❌ Local video element not found');
                return;
            }
            
            console.log('✅ Video initialized');
            
        } catch (error) {
            console.error('❌ Failed to initialize video:', error);
        }
    }
    
    sendChatMessage() {
        const chatInput = document.getElementById('chat-input');
        const participantInput = document.getElementById('participant-name');
        
        if (!chatInput || !chatInput.value.trim()) {
            return;
        }
        
        const message = chatInput.value.trim();
        const participant = participantInput ? participantInput.value : 'Anonymous';
        
        // Add message to chat
        this.addChatMessage(participant, message, 'sent');
        
        // Clear input
        chatInput.value = '';
        
        console.log('💬 Chat message sent:', message);
    }
    
    addChatMessage(sender, message, type = 'received') {
        const chatContainer = document.getElementById('chatContainer');
        if (!chatContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    generateConferenceId() {
        return 'SEEKER-' + Math.random().toString(36).substr(2, 9).toUpperCase();
    }
}

// Make available globally
window.SEEKERVideoConference = SEEKERVideoConference; 
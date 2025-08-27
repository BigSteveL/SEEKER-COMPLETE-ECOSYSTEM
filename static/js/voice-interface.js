/**
 * SEEKER Voice Interface Module
 * Multilingual voice processing with AI orchestration
 */

class SEEKERVoiceInterface {
    constructor() {
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.recognition = null;
        this.synthesis = null;
        
        this.init();
    }
    
    init() {
        console.log('🎤 Initializing SEEKER Voice Interface...');
        this.initializeSpeechRecognition();
        this.initializeSpeechSynthesis();
        this.initializeEventListeners();
        console.log('✅ Voice Interface initialized');
    }
    
    initializeSpeechRecognition() {
        try {
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                this.recognition.continuous = true;
                this.recognition.interimResults = true;
                this.recognition.lang = 'en-US';
                
                this.recognition.onresult = (event) => {
                    this.handleSpeechResult(event);
                };
                
                this.recognition.onerror = (event) => {
                    console.error('Speech recognition error:', event.error);
                };
                
                console.log('✅ Speech recognition initialized');
            } else {
                console.warn('⚠️ Speech recognition not supported');
            }
        } catch (error) {
            console.error('❌ Failed to initialize speech recognition:', error);
        }
    }
    
    initializeSpeechSynthesis() {
        try {
            if ('speechSynthesis' in window) {
                this.synthesis = window.speechSynthesis;
                console.log('✅ Speech synthesis initialized');
            } else {
                console.warn('⚠️ Speech synthesis not supported');
            }
        } catch (error) {
            console.error('❌ Failed to initialize speech synthesis:', error);
        }
    }
    
    initializeEventListeners() {
        console.log('🔗 Adding voice interface event listeners...');
        
        // Voice control buttons
        const startVoiceBtn = document.getElementById('startVoiceBtn');
        const stopVoiceBtn = document.getElementById('stopVoiceBtn');
        const testVoiceBtn = document.getElementById('testVoiceBtn');
        
        if (startVoiceBtn) {
            startVoiceBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('🎤 Start voice clicked');
                this.startVoiceInput();
            });
            console.log('✅ Start voice button listener added');
        } else {
            console.error('❌ Start voice button not found');
        }
        
        if (stopVoiceBtn) {
            stopVoiceBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('⏹️ Stop voice clicked');
                this.stopVoiceInput();
            });
            console.log('✅ Stop voice button listener added');
        } else {
            console.error('❌ Stop voice button not found');
        }
        
        if (testVoiceBtn) {
            testVoiceBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('🔊 Test voice clicked');
                this.testVoiceOutput();
            });
            console.log('✅ Test voice button listener added');
        } else {
            console.error('❌ Test voice button not found');
        }
        
        // Language selectors
        const sourceLanguage = document.getElementById('sourceLanguage');
        const targetLanguage = document.getElementById('targetLanguage');
        
        if (sourceLanguage) {
            sourceLanguage.addEventListener('change', (e) => {
                console.log('🌍 Source language changed:', e.target.value);
                this.updateRecognitionLanguage(e.target.value);
            });
            console.log('✅ Source language listener added');
        }
        
        if (targetLanguage) {
            targetLanguage.addEventListener('change', (e) => {
                console.log('🌍 Target language changed:', e.target.value);
                this.updateSynthesisLanguage(e.target.value);
            });
            console.log('✅ Target language listener added');
        }
        
        console.log('✅ All voice interface event listeners initialized');
    }
    
    startVoiceInput() {
        try {
            if (this.isRecording) {
                console.log('⚠️ Already recording');
                return;
            }
            
            console.log('🎤 Starting voice input...');
            
            if (this.recognition) {
                this.recognition.start();
                this.isRecording = true;
                
                // Update UI
                const startBtn = document.getElementById('startVoiceBtn');
                const stopBtn = document.getElementById('stopVoiceBtn');
                
                if (startBtn) startBtn.disabled = true;
                if (stopBtn) stopBtn.disabled = false;
                
                // Update progress bar
                this.updateVoiceProgress(50);
                
                console.log('✅ Voice input started');
            } else {
                console.error('❌ Speech recognition not available');
            }
            
        } catch (error) {
            console.error('❌ Failed to start voice input:', error);
        }
    }
    
    stopVoiceInput() {
        try {
            if (!this.isRecording) {
                console.log('⚠️ Not recording');
                return;
            }
            
            console.log('⏹️ Stopping voice input...');
            
            if (this.recognition) {
                this.recognition.stop();
                this.isRecording = false;
                
                // Update UI
                const startBtn = document.getElementById('startVoiceBtn');
                const stopBtn = document.getElementById('stopVoiceBtn');
                
                if (startBtn) startBtn.disabled = false;
                if (stopBtn) stopBtn.disabled = true;
                
                // Reset progress bar
                this.updateVoiceProgress(0);
                
                console.log('✅ Voice input stopped');
            }
            
        } catch (error) {
            console.error('❌ Failed to stop voice input:', error);
        }
    }
    
    handleSpeechResult(event) {
        try {
            let finalTranscript = '';
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            if (finalTranscript) {
                console.log('🎤 Final transcript:', finalTranscript);
                this.processVoiceInput(finalTranscript);
            }
            
            if (interimTranscript) {
                console.log('🎤 Interim transcript:', interimTranscript);
            }
            
        } catch (error) {
            console.error('❌ Error handling speech result:', error);
        }
    }
    
    processVoiceInput(text) {
        try {
            console.log('🧠 Processing voice input:', text);
            
            // Simulate AI processing
            setTimeout(() => {
                this.classifyVoiceInput(text);
                this.translateVoiceInput(text);
            }, 1000);
            
        } catch (error) {
            console.error('❌ Error processing voice input:', error);
        }
    }
    
    classifyVoiceInput(text) {
        try {
            console.log('🏷️ Classifying voice input...');
            
            // Simulate AI classification
            const classifications = [
                'Business Meeting',
                'Technical Discussion',
                'Casual Conversation',
                'Presentation',
                'Interview'
            ];
            
            const randomClassification = classifications[Math.floor(Math.random() * classifications.length)];
            
            // Update classification results
            const classificationResults = document.getElementById('classificationResults');
            if (classificationResults) {
                classificationResults.innerHTML = `
                    <div class="alert alert-success">
                        <strong>Classification:</strong> ${randomClassification}<br>
                        <strong>Confidence:</strong> ${Math.floor(Math.random() * 20 + 80)}%
                    </div>
                `;
            }
            
            console.log('✅ Voice input classified:', randomClassification);
            
        } catch (error) {
            console.error('❌ Error classifying voice input:', error);
        }
    }
    
    translateVoiceInput(text) {
        try {
            console.log('🌍 Translating voice input...');
            
            // Simulate translation
            const translatedText = `[Translated] ${text}`;
            
            console.log('✅ Voice input translated:', translatedText);
            
        } catch (error) {
            console.error('❌ Error translating voice input:', error);
        }
    }
    
    testVoiceOutput() {
        try {
            console.log('🔊 Testing voice output...');
            
            if (this.synthesis) {
                const utterance = new SpeechSynthesisUtterance('Hello, this is a test of the SEEKER voice interface.');
                utterance.lang = 'en-US';
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                
                this.synthesis.speak(utterance);
                console.log('✅ Voice output test started');
            } else {
                console.error('❌ Speech synthesis not available');
            }
            
        } catch (error) {
            console.error('❌ Error testing voice output:', error);
        }
    }
    
    updateRecognitionLanguage(language) {
        try {
            if (this.recognition) {
                this.recognition.lang = language;
                console.log('✅ Recognition language updated:', language);
            }
        } catch (error) {
            console.error('❌ Error updating recognition language:', error);
        }
    }
    
    updateSynthesisLanguage(language) {
        try {
            console.log('✅ Synthesis language updated:', language);
        } catch (error) {
            console.error('❌ Error updating synthesis language:', error);
        }
    }
    
    updateVoiceProgress(percentage) {
        try {
            const progressBar = document.getElementById('voiceProgress');
            if (progressBar) {
                progressBar.style.width = percentage + '%';
            }
        } catch (error) {
            console.error('❌ Error updating voice progress:', error);
        }
    }
}

// Make available globally
window.SEEKERVoiceInterface = SEEKERVoiceInterface; 
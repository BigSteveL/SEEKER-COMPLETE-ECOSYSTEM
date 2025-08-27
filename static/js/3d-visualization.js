/**
 * SEEKER 3D Visualization Module
 * Advanced 3D design and prototyping with AI optimization
 * Integrated with holographic projection system
 */

class SEEKER3DVisualization {
    constructor(containerId) {
        this.containerId = containerId;
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.currentModel = null;
        this.collaborators = [];
        this.aiSuggestions = [];
        this.designIterations = [];
        this.holographicProjection = null; // Add holographic integration
        this.isHolographicConnected = false;
        
        this.init();
    }
    
    async init() {
        try {
            console.log('🎨 Initializing SEEKER 3D Visualization...');
            
            // Initialize Three.js scene
            this.initializeScene();
            
            // Initialize SEEKER features
            this.initializeSEEKERFeatures();
            
            // Initialize holographic integration
            await this.initializeHolographicIntegration();
            
            // Initialize event listeners
            this.initializeEventListeners();
            
            console.log('✅ SEEKER 3D Visualization initialized');
            
        } catch (error) {
            console.error('❌ Failed to initialize 3D visualization:', error);
        }
    }
    
    initializeScene() {
        // Create Three.js scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a2e);
        
        // Create camera
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.camera.position.set(5, 5, 5);
        
        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(800, 600);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        
        // Add renderer to container
        const container = document.getElementById(this.containerId);
        if (container) {
            container.appendChild(this.renderer.domElement);
        }
        
        // Add controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        
        // Add lighting
        this.addLighting();
        
        // Add grid
        this.addGrid();
        
        // Start render loop
        this.animate();
    }
    
    addLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(10, 10, 5);
        directionalLight.castShadow = true;
        this.scene.add(directionalLight);
        
        // Point light
        const pointLight = new THREE.PointLight(0x00d4aa, 1, 100);
        pointLight.position.set(0, 10, 0);
        this.scene.add(pointLight);
    }
    
    addGrid() {
        const gridHelper = new THREE.GridHelper(20, 20, 0x444444, 0x222222);
        this.scene.add(gridHelper);
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
    
    initializeSEEKERFeatures() {
        // Initialize design iteration tracking
        this.designIterations = [];
        
        // Initialize manufacturing connections
        this.manufacturingConnections = [
            { id: 'mfg_1', name: 'Global 3D Printing Hub', location: 'Asia', capacity: 'High', cost: 'Low' },
            { id: 'mfg_2', name: 'Precision Manufacturing', location: 'Europe', capacity: 'Medium', cost: 'Medium' },
            { id: 'mfg_3', name: 'Rapid Prototyping Lab', location: 'North America', capacity: 'Low', cost: 'High' }
        ];
        
        // Initialize production workflows
        this.productionWorkflows = [
            { id: 'wf_1', name: 'Rapid Prototyping', steps: ['Design', '3D Print', 'Test', 'Iterate'] },
            { id: 'wf_2', name: 'Mass Production', steps: ['Design', 'Mold', 'Injection', 'Assembly', 'Quality'] },
            { id: 'wf_3', name: 'Custom Manufacturing', steps: ['Design', 'CNC', 'Finishing', 'Quality'] }
        ];
        
        // Initialize AI suggestions
        this.aiSuggestions = [
            { id: 'sug_1', type: 'material', title: 'Material Optimization', description: 'Consider switching to PETG for better strength-to-weight ratio', impact: 'high' },
            { id: 'sug_2', type: 'structural', title: 'Structural Improvement', description: 'Add internal supports to reduce material usage by 15%', impact: 'medium' },
            { id: 'sug_3', type: 'cost', title: 'Cost Optimization', description: 'Use infill optimization to reduce material cost by 20%', impact: 'high' }
        ];
    }
    
    async initializeHolographicIntegration() {
        try {
            console.log('🔮 Initializing holographic integration...');
            
            // Check if holographic system is available
            const response = await fetch('/api/v1/holographic/devices');
            if (response.ok) {
                const result = await response.json();
                if (result.success && result.data.devices.length > 0) {
                    this.isHolographicConnected = true;
                    this.holographicDevices = result.data.devices;
                    
                    // Add holographic controls to 3D tab
                    this.addHolographicControls();
                    
                    // Populate device dropdown
                    this.populateDeviceDropdown();
                    
                    // Add event listeners for holographic controls
                    this.addHolographicEventListeners();
                    
                    console.log('✅ Holographic integration successful');
                } else {
                    console.log('⚠️ No holographic devices available');
                }
            } else {
                console.log('⚠️ Holographic API not available');
            }
            
        } catch (error) {
            console.error('❌ Holographic integration failed:', error);
        }
    }
    
    addHolographicControls() {
        // Find the 3D tab content area
        const threeDTab = document.getElementById('3d');
        if (!threeDTab) {
            console.error('❌ 3D tab not found');
            return;
        }
        
        // Find the right column (col-md-4) to add holographic controls
        const rightColumn = threeDTab.querySelector('.col-md-4');
        if (!rightColumn) {
            console.error('❌ Right column not found in 3D tab');
            return;
        }
        
        // Add holographic section to 3D tab
        const holographicSection = document.createElement('div');
        holographicSection.className = 'card mt-3';
        holographicSection.innerHTML = `
            <div class="card-body">
                <h5><i class="fas fa-hologram me-2"></i>Holographic Projection</h5>
                <div class="holographic-status mb-3">
                    <span class="status-indicator ${this.isHolographicConnected ? 'status-online' : 'status-offline'}"></span>
                    <span>${this.isHolographicConnected ? 'Connected' : 'Disconnected'}</span>
                    ${this.isHolographicConnected ? `<small class="text-muted ms-2">(${this.holographicDevices.length} devices available)</small>` : ''}
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <button class="btn btn-primary w-100" id="projectToHolographic">
                            <i class="fas fa-hologram me-2"></i>Project to Holographic
                        </button>
                    </div>
                    <div class="col-md-6">
                        <button class="btn btn-secondary w-100" id="enableHolographicCollaboration">
                            <i class="fas fa-users me-2"></i>Enable Collaboration
                        </button>
                    </div>
                </div>
                <div class="mt-3">
                    <label class="form-label">Select Holographic Device:</label>
                    <select class="form-select" id="holographicDevice">
                        <option value="">Choose a device...</option>
                    </select>
                </div>
                <div class="mt-3">
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="realTimeStreaming" checked>
                        <label class="form-check-label" for="realTimeStreaming">
                            Real-time Streaming
                        </label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" id="interactiveMode">
                        <label class="form-check-label" for="interactiveMode">
                            Interactive Mode
                        </label>
                    </div>
                </div>
                <div class="mt-3">
                    <small class="text-muted">
                        <i class="fas fa-info-circle me-1"></i>
                        Project your 3D design to holographic displays for immersive collaboration
                    </small>
                </div>
            </div>
        `;
        
        // Append to the right column
        rightColumn.appendChild(holographicSection);
        console.log('✅ Holographic controls added to 3D tab');
    }
    
    populateDeviceDropdown() {
        const deviceSelect = document.getElementById('holographicDevice');
        if (deviceSelect && this.holographicDevices) {
            // Clear existing options
            deviceSelect.innerHTML = '<option value="">Choose a device...</option>';
            
            // Add device options
            this.holographicDevices.forEach(device => {
                const option = document.createElement('option');
                option.value = device.device_id;
                option.textContent = `${device.name} (${device.type})`;
                deviceSelect.appendChild(option);
            });
        }
    }
    
    addHolographicEventListeners() {
        console.log('🔗 Adding holographic event listeners...');
        
        // Project to holographic button
        const projectBtn = document.getElementById('projectToHolographic');
        const collaborationBtn = document.getElementById('enableHolographicCollaboration');
        const deviceSelect = document.getElementById('holographicDevice');
        const realTimeCheckbox = document.getElementById('realTimeStreaming');
        const interactiveCheckbox = document.getElementById('interactiveMode');
        
        if (projectBtn) {
            projectBtn.addEventListener('click', async (e) => {
                e.preventDefault();
                console.log('🎬 Project to holographic clicked');
                await this.projectToHolographic();
            });
            console.log('✅ Project button listener added');
        } else {
            console.error('❌ Project button not found');
        }
        
        if (collaborationBtn) {
            collaborationBtn.addEventListener('click', async (e) => {
                e.preventDefault();
                console.log('👥 Enable collaboration clicked');
                await this.enableHolographicCollaboration();
            });
            console.log('✅ Collaboration button listener added');
        } else {
            console.error('❌ Collaboration button not found');
        }
        
        if (deviceSelect) {
            deviceSelect.addEventListener('change', (e) => {
                console.log('📱 Device selected:', e.target.value);
                this.selectHolographicDevice(e.target.value);
            });
            console.log('✅ Device select listener added');
        } else {
            console.error('❌ Device select not found');
        }
        
        if (realTimeCheckbox) {
            realTimeCheckbox.addEventListener('change', (e) => {
                console.log('📡 Real-time streaming toggled:', e.target.checked);
                this.toggleRealTimeStreaming(e.target.checked);
            });
            console.log('✅ Real-time checkbox listener added');
        } else {
            console.error('❌ Real-time checkbox not found');
        }
        
        if (interactiveCheckbox) {
            interactiveCheckbox.addEventListener('change', (e) => {
                console.log('🎮 Interactive mode toggled:', e.target.checked);
                this.toggleInteractiveMode(e.target.checked);
            });
            console.log('✅ Interactive checkbox listener added');
        } else {
            console.error('❌ Interactive checkbox not found');
        }
        
        console.log('✅ All holographic event listeners added');
    }
    
    async projectToHolographic() {
        try {
            if (!this.isHolographicConnected) {
                this.showNotification('Holographic system not connected', 'error');
                return;
            }
            
            const deviceId = document.getElementById('holographicDevice').value;
            if (!deviceId) {
                this.showNotification('Please select a holographic device', 'error');
                return;
            }
            
            // Show loading state
            const projectBtn = document.getElementById('projectToHolographic');
            const originalText = projectBtn.innerHTML;
            projectBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Projecting...';
            projectBtn.disabled = true;
            
            // Export current 3D model
            const modelData = this.exportCurrentModel();
            
            // Get projection settings
            const isRealTime = document.getElementById('realTimeStreaming')?.checked || false;
            const isInteractive = document.getElementById('interactiveMode')?.checked || false;
            
            // Create holographic projection
            const response = await fetch('/api/v1/holographic/projections', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    device_id: deviceId,
                    model_data: modelData || 'default_cube_model',
                    projection_type: isRealTime ? 'real_time_stream' : 'static_3d',
                    is_interactive: isInteractive,
                    quality_preset: 'presentation'
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showNotification('Successfully projected to holographic device!', 'success');
                console.log('Holographic projection created:', result);
                
                // Update UI to show active projection
                this.updateProjectionStatus(result.data.projection_id);
            } else {
                const errorData = await response.json();
                this.showNotification(`Failed to create projection: ${errorData.message || 'Unknown error'}`, 'error');
            }
            
        } catch (error) {
            console.error('Holographic projection failed:', error);
            this.showNotification('Holographic projection failed: ' + error.message, 'error');
        } finally {
            // Restore button state
            const projectBtn = document.getElementById('projectToHolographic');
            if (projectBtn) {
                projectBtn.innerHTML = '<i class="fas fa-hologram me-2"></i>Project to Holographic';
                projectBtn.disabled = false;
            }
        }
    }
    
    async enableHolographicCollaboration() {
        try {
            if (!this.isHolographicConnected) {
                this.showNotification('Holographic system not connected', 'error');
                return;
            }
            
            const deviceId = document.getElementById('holographicDevice').value;
            if (!deviceId) {
                this.showNotification('Please select a holographic device first', 'error');
                return;
            }
            
            // Show loading state
            const collabBtn = document.getElementById('enableHolographicCollaboration');
            const originalText = collabBtn.innerHTML;
            collabBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enabling...';
            collabBtn.disabled = true;
            
            // Enable collaborative mode
            const response = await fetch('/api/v1/holographic/collaboration/enable', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    device_id: deviceId,
                    session_id: this.generateSessionId(),
                    max_participants: 5,
                    collaboration_type: 'real_time_3d'
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showNotification('Collaborative mode enabled! Share session ID: ' + result.data.session_id, 'success');
                this.startCollaborativeSession(result.data.session_id);
            } else {
                const errorData = await response.json();
                this.showNotification(`Failed to enable collaboration: ${errorData.message || 'Unknown error'}`, 'error');
            }
            
        } catch (error) {
            console.error('Collaboration setup failed:', error);
            this.showNotification('Collaboration setup failed: ' + error.message, 'error');
        } finally {
            // Restore button state
            const collabBtn = document.getElementById('enableHolographicCollaboration');
            if (collabBtn) {
                collabBtn.innerHTML = '<i class="fas fa-users me-2"></i>Enable Collaboration';
                collabBtn.disabled = false;
            }
        }
    }
    
    selectHolographicDevice(deviceId) {
        console.log('Selected holographic device:', deviceId);
        
        if (deviceId) {
            const device = this.holographicDevices.find(d => d.device_id === deviceId);
            if (device) {
                this.showNotification(`Connected to ${device.name}`, 'success');
                
                // Update device status
                this.updateDeviceStatus(device);
            }
        }
    }
    
    toggleRealTimeStreaming(enabled) {
        console.log('Real-time streaming:', enabled ? 'enabled' : 'disabled');
        this.showNotification(`Real-time streaming ${enabled ? 'enabled' : 'disabled'}`, 'info');
    }
    
    toggleInteractiveMode(enabled) {
        console.log('Interactive mode:', enabled ? 'enabled' : 'disabled');
        this.showNotification(`Interactive mode ${enabled ? 'enabled' : 'disabled'}`, 'info');
    }
    
    updateDeviceStatus(device) {
        // Update device status display
        const statusElement = document.querySelector('.holographic-status span');
        if (statusElement) {
            statusElement.innerHTML = `<span class="status-indicator status-online"></span>Connected to ${device.name}`;
        }
    }
    
    updateProjectionStatus(projectionId) {
        // Add projection status indicator
        const projectionStatus = document.createElement('div');
        projectionStatus.className = 'alert alert-success mt-3';
        projectionStatus.innerHTML = `
            <i class="fas fa-hologram me-2"></i>
            <strong>Active Projection:</strong> ${projectionId}
            <button class="btn btn-sm btn-outline-danger ms-2" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        const holographicSection = document.querySelector('.card-body');
        if (holographicSection) {
            holographicSection.appendChild(projectionStatus);
        }
    }
    
    exportCurrentModel() {
        // Export current 3D model for holographic projection
        if (this.currentModel) {
            const exporter = new THREE.STLExporter();
            return exporter.parse(this.currentModel);
        }
        return null;
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    startCollaborativeSession(sessionId) {
        // Initialize collaborative session
        console.log('Starting collaborative session...');
        this.showNotification(`Collaborative session started with ID: ${sessionId}`, 'success');
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} alert-dismissible fade show`;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Add to page
        const container = document.querySelector('.container');
        if (container) {
            container.insertBefore(notification, container.firstChild);
            
            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 5000);
        }
    }
    
    initializeEventListeners() {
        console.log('🔗 Initializing 3D visualization event listeners...');
        
        // 3D Visualization controls
        const resetViewBtn = document.getElementById('resetViewBtn');
        const exportDesignBtn = document.getElementById('exportDesignBtn');
        const createPrototypeBtn = document.getElementById('createPrototypeBtn');
        const applyParametersBtn = document.getElementById('applyParametersBtn');
        
        if (resetViewBtn) {
            resetViewBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('🔄 Reset view clicked');
                this.resetView();
            });
            console.log('✅ Reset view button listener added');
        } else {
            console.error('❌ Reset view button not found');
        }
        
        if (exportDesignBtn) {
            exportDesignBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('📤 Export design clicked');
                this.exportDesign();
            });
            console.log('✅ Export design button listener added');
        } else {
            console.error('❌ Export design button not found');
        }
        
        if (createPrototypeBtn) {
            createPrototypeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('➕ Create prototype clicked');
                this.createNewPrototype();
            });
            console.log('✅ Create prototype button listener added');
        } else {
            console.error('❌ Create prototype button not found');
        }
        
        if (applyParametersBtn) {
            applyParametersBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('🎯 Apply parameters clicked');
                this.applyAIOptimization();
            });
            console.log('✅ Apply parameters button listener added');
        } else {
            console.error('❌ Apply parameters button not found');
        }
        
        // Material, complexity, and quality selectors
        const materialSelect = document.getElementById('materialSelect');
        const complexitySelect = document.getElementById('complexitySelect');
        const qualitySelect = document.getElementById('qualitySelect');
        
        if (materialSelect) {
            materialSelect.addEventListener('change', (e) => {
                console.log('🧱 Material changed:', e.target.value);
                this.updateDesignMetrics();
            });
            console.log('✅ Material select listener added');
        }
        
        if (complexitySelect) {
            complexitySelect.addEventListener('change', (e) => {
                console.log('⚙️ Complexity changed:', e.target.value);
                this.updateDesignMetrics();
            });
            console.log('✅ Complexity select listener added');
        }
        
        if (qualitySelect) {
            qualitySelect.addEventListener('change', (e) => {
                console.log('⭐ Quality changed:', e.target.value);
                this.updateDesignMetrics();
            });
            console.log('✅ Quality select listener added');
        }
        
        console.log('✅ All 3D visualization event listeners initialized');
    }
    
    resetView() {
        this.camera.position.set(5, 5, 5);
        this.controls.reset();
    }
    
    exportDesign() {
        if (this.currentModel) {
            const exporter = new THREE.STLExporter();
            const stlData = exporter.parse(this.currentModel);
            
            const blob = new Blob([stlData], { type: 'application/octet-stream' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = 'seeker_design.stl';
            a.click();
            
            URL.revokeObjectURL(url);
        }
    }
    
    createNewPrototype() {
        // Clear current scene
        this.scene.clear();
        this.addLighting();
        this.addGrid();
        
        // Create new prototype
        this.createBasicPrototype();
    }
    
    createBasicPrototype() {
        // Create a basic cube as starting point
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshPhongMaterial({ color: 0x00d4aa });
        this.currentModel = new THREE.Mesh(geometry, material);
        this.currentModel.castShadow = true;
        this.currentModel.receiveShadow = true;
        
        this.scene.add(this.currentModel);
    }
    
    applyAIOptimization() {
        // Apply AI optimization to current design
        console.log('Applying AI optimization...');
        
        // Simulate AI optimization
        setTimeout(() => {
            this.updateDesignMetrics();
            this.showNotification('AI optimization applied successfully', 'success');
        }, 2000);
    }
    
    updateDesignMetrics() {
        // Update design metrics display
        const strengthMetric = document.getElementById('strengthMetric');
        const weightMetric = document.getElementById('weightMetric');
        const costMetric = document.getElementById('costMetric');
        const timeMetric = document.getElementById('timeMetric');
        
        if (strengthMetric) strengthMetric.textContent = '92%';
        if (weightMetric) weightMetric.textContent = '1.8kg';
        if (costMetric) costMetric.textContent = '$38';
        if (timeMetric) timeMetric.textContent = '3.5h';
    }

    // Add method to handle tab activation
    onTabActivated() {
        console.log('🎨 3D Visualization tab activated');
        
        // Ensure the scene is properly sized
        if (this.renderer && this.containerId) {
            const container = document.getElementById(this.containerId);
            if (container) {
                const rect = container.getBoundingClientRect();
                this.renderer.setSize(rect.width, rect.height);
                this.camera.aspect = rect.width / rect.height;
                this.camera.updateProjectionMatrix();
            }
        }
        
        // Update design metrics
        this.updateDesignMetrics();
        
        // Check holographic connection status
        if (this.isHolographicConnected) {
            this.showNotification('🔮 Holographic system connected and ready', 'success');
        } else {
            this.showNotification('⚠️ Holographic system not available', 'warning');
        }
    }
}

// Make available globally
window.SEEKER3DVisualization = SEEKER3DVisualization; 
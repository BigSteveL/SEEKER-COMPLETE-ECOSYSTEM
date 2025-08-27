/**
 * SEEKER Holographic Projection Frontend
 * Real-time 3D holographic displays for business presentations
 */

class SEEKERHolographicProjection {
    constructor() {
        this.devices = [];
        this.activeProjections = [];
        this.websocketConnections = {};
        this.currentScenario = null;
        this.isInitialized = false;
        
        this.init();
    }
    
    async init() {
        try {
            console.log('🔮 Initializing SEEKER Holographic Projection...');
            
            // Initialize UI components
            this.initializeUI();
            
            // Load available devices
            await this.loadDevices();
            
            // Load business scenarios
            await this.loadBusinessScenarios();
            
            this.isInitialized = true;
            console.log('✅ SEEKER Holographic Projection initialized');
            
        } catch (error) {
            console.error('❌ Failed to initialize holographic projection:', error);
        }
    }
    
    initializeUI() {
        // Create holographic projection panel
        this.createHolographicPanel();
        
        // Create device management panel
        this.createDevicePanel();
        
        // Create business scenarios panel
        this.createScenariosPanel();
        
        // Create projection controls
        this.createProjectionControls();
    }
    
    createHolographicPanel() {
        const panel = document.createElement('div');
        panel.id = 'holographic-panel';
        panel.className = 'holographic-panel';
        panel.innerHTML = `
            <div class="panel-header">
                <h3>🔮 SEEKER Holographic Projection</h3>
                <div class="panel-controls">
                    <button id="refresh-devices" class="btn btn-secondary">🔄 Refresh</button>
                    <button id="toggle-panel" class="btn btn-primary">📱 Toggle Panel</button>
                </div>
            </div>
            <div class="panel-content">
                <div class="holographic-status">
                    <div class="status-indicator" id="holo-status">🔴 Disconnected</div>
                    <div class="device-count" id="device-count">Devices: 0</div>
                    <div class="projection-count" id="projection-count">Projections: 0</div>
                </div>
                <div class="holographic-controls">
                    <div class="control-section">
                        <h4>📱 Device Management</h4>
                        <div id="device-list" class="device-list"></div>
                    </div>
                    <div class="control-section">
                        <h4>🎬 Active Projections</h4>
                        <div id="projection-list" class="projection-list"></div>
                    </div>
                    <div class="control-section">
                        <h4>💼 Business Scenarios</h4>
                        <div id="scenarios-list" class="scenarios-list"></div>
                    </div>
                </div>
            </div>
        `;
        
        // Add to main interface
        const mainContainer = document.querySelector('.main-container') || document.body;
        mainContainer.appendChild(panel);
        
        // Add event listeners
        this.addPanelEventListeners();
    }
    
    createDevicePanel() {
        const devicePanel = document.createElement('div');
        devicePanel.id = 'device-management-panel';
        devicePanel.className = 'device-panel';
        devicePanel.innerHTML = `
            <div class="panel-header">
                <h4>📱 Holographic Devices</h4>
            </div>
            <div class="device-grid" id="device-grid"></div>
        `;
        
        document.getElementById('holographic-panel').querySelector('.panel-content').appendChild(devicePanel);
    }
    
    createScenariosPanel() {
        const scenariosPanel = document.createElement('div');
        scenariosPanel.id = 'business-scenarios-panel';
        scenariosPanel.className = 'scenarios-panel';
        scenariosPanel.innerHTML = `
            <div class="panel-header">
                <h4>💼 Business Scenarios</h4>
            </div>
            <div class="scenarios-grid" id="scenarios-grid"></div>
        `;
        
        document.getElementById('holographic-panel').querySelector('.panel-content').appendChild(scenariosPanel);
    }
    
    createProjectionControls() {
        const controlsPanel = document.createElement('div');
        controlsPanel.id = 'projection-controls-panel';
        controlsPanel.className = 'controls-panel';
        controlsPanel.innerHTML = `
            <div class="panel-header">
                <h4>🎬 Projection Controls</h4>
            </div>
            <div class="control-grid">
                <div class="control-group">
                    <label>Device:</label>
                    <select id="projection-device" class="form-control">
                        <option value="">Select Device</option>
                    </select>
                </div>
                <div class="control-group">
                    <label>Model URL:</label>
                    <input type="text" id="model-url" class="form-control" placeholder="Enter 3D model URL">
                </div>
                <div class="control-group">
                    <label>Projection Type:</label>
                    <select id="projection-type" class="form-control">
                        <option value="static_3d">Static 3D</option>
                        <option value="animated_3d">Animated 3D</option>
                        <option value="interactive_3d">Interactive 3D</option>
                        <option value="real_time_stream">Real-time Stream</option>
                    </select>
                </div>
                <div class="control-group">
                    <label>Interactive:</label>
                    <input type="checkbox" id="is-interactive" class="form-checkbox">
                </div>
                <div class="control-actions">
                    <button id="create-projection" class="btn btn-success">🎬 Create Projection</button>
                    <button id="start-streaming" class="btn btn-info">📡 Start Streaming</button>
                    <button id="enable-collaborative" class="btn btn-warning">👥 Enable Collaborative</button>
                </div>
            </div>
        `;
        
        document.getElementById('holographic-panel').querySelector('.panel-content').appendChild(controlsPanel);
        
        // Add control event listeners
        this.addControlEventListeners();
    }
    
    addPanelEventListeners() {
        document.getElementById('refresh-devices').addEventListener('click', () => {
            this.loadDevices();
        });
        
        document.getElementById('toggle-panel').addEventListener('click', () => {
            const panel = document.getElementById('holographic-panel');
            panel.classList.toggle('collapsed');
        });
    }
    
    addControlEventListeners() {
        document.getElementById('create-projection').addEventListener('click', () => {
            this.createProjection();
        });
        
        document.getElementById('start-streaming').addEventListener('click', () => {
            this.startRealTimeStreaming();
        });
        
        document.getElementById('enable-collaborative').addEventListener('click', () => {
            this.enableCollaborativeMode();
        });
    }
    
    async loadDevices() {
        try {
            const response = await fetch('/api/v1/holographic/devices');
            const result = await response.json();
            
            if (result.success) {
                this.devices = result.data.devices;
                this.updateDeviceDisplay();
                this.updateStatus();
                console.log('📱 Loaded holographic devices:', this.devices);
            } else {
                console.error('❌ Failed to load devices:', result.message);
            }
        } catch (error) {
            console.error('❌ Error loading devices:', error);
        }
    }
    
    async loadBusinessScenarios() {
        try {
            const response = await fetch('/api/v1/holographic/business-scenarios');
            const result = await response.json();
            
            if (result.success) {
                this.businessScenarios = result.data.scenarios;
                this.updateScenariosDisplay();
                console.log('💼 Loaded business scenarios:', this.businessScenarios);
            } else {
                console.error('❌ Failed to load scenarios:', result.message);
            }
        } catch (error) {
            console.error('❌ Error loading scenarios:', error);
        }
    }
    
    updateDeviceDisplay() {
        const deviceGrid = document.getElementById('device-grid');
        const deviceSelect = document.getElementById('projection-device');
        
        // Update device grid
        deviceGrid.innerHTML = this.devices.map(device => `
            <div class="device-card ${device.is_active ? 'active' : 'inactive'}">
                <div class="device-header">
                    <h5>${device.name}</h5>
                    <span class="device-type">${device.type}</span>
                </div>
                <div class="device-details">
                    <div class="detail-item">
                        <span class="label">Resolution:</span>
                        <span class="value">${device.resolution.join(' x ')}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">Refresh Rate:</span>
                        <span class="value">${device.refresh_rate} Hz</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">Status:</span>
                        <span class="status ${device.is_active ? 'active' : 'inactive'}">
                            ${device.is_active ? '🟢 Active' : '🔴 Inactive'}
                        </span>
                    </div>
                </div>
                <div class="device-actions">
                    <button class="btn btn-sm btn-primary" onclick="holographicProjection.getDeviceStatus('${device.device_id}')">
                        📊 Status
                    </button>
                </div>
            </div>
        `).join('');
        
        // Update device select
        deviceSelect.innerHTML = '<option value="">Select Device</option>' + 
            this.devices.map(device => 
                `<option value="${device.device_id}">${device.name}</option>`
            ).join('');
    }
    
    updateScenariosDisplay() {
        const scenariosGrid = document.getElementById('scenarios-grid');
        
        scenariosGrid.innerHTML = this.businessScenarios.map(scenario => `
            <div class="scenario-card">
                <div class="scenario-header">
                    <h5>${scenario.name}</h5>
                    <span class="scenario-id">${scenario.id}</span>
                </div>
                <div class="scenario-description">
                    ${scenario.description}
                </div>
                <div class="scenario-use-cases">
                    <h6>Use Cases:</h6>
                    <ul>
                        ${scenario.use_cases.map(useCase => `<li>${useCase}</li>`).join('')}
                    </ul>
                </div>
                <div class="scenario-actions">
                    <button class="btn btn-sm btn-success" onclick="holographicProjection.activateScenario('${scenario.id}')">
                        🚀 Activate
                    </button>
                    <button class="btn btn-sm btn-info" onclick="holographicProjection.viewScenarioDetails('${scenario.id}')">
                        📋 Details
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    updateStatus() {
        document.getElementById('holo-status').textContent = this.isInitialized ? '🟢 Connected' : '🔴 Disconnected';
        document.getElementById('device-count').textContent = `Devices: ${this.devices.length}`;
        document.getElementById('projection-count').textContent = `Projections: ${this.activeProjections.length}`;
    }
    
    async createProjection() {
        try {
            const deviceId = document.getElementById('projection-device').value;
            const modelUrl = document.getElementById('model-url').value;
            const projectionType = document.getElementById('projection-type').value;
            const isInteractive = document.getElementById('is-interactive').checked;
            
            if (!deviceId || !modelUrl) {
                alert('Please select a device and enter a model URL');
                return;
            }
            
            const request = {
                device_id: deviceId,
                projection_type: projectionType,
                model_url: modelUrl,
                position: [0.0, 0.0, 0.0],
                rotation: [0.0, 0.0, 0.0],
                scale: 1.0,
                is_interactive: isInteractive
            };
            
            const response = await fetch('/api/v1/holographic/projections', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(request)
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('✅ Projection created:', result.data);
                this.activeProjections.push(result.data);
                this.updateProjectionDisplay();
                this.updateStatus();
                
                // Show success message
                this.showNotification('Projection created successfully!', 'success');
            } else {
                console.error('❌ Failed to create projection:', result.message);
                this.showNotification('Failed to create projection', 'error');
            }
        } catch (error) {
            console.error('❌ Error creating projection:', error);
            this.showNotification('Error creating projection', 'error');
        }
    }
    
    async startRealTimeStreaming() {
        try {
            const projectionId = this.getSelectedProjectionId();
            if (!projectionId) {
                alert('Please select a projection first');
                return;
            }
            
            const streamConfig = {
                quality: 'presentation',
                latency_target: 16,
                enable_interaction: true
            };
            
            const response = await fetch(`/api/v1/holographic/projections/${projectionId}/streaming`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(streamConfig)
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('📡 Real-time streaming started:', result.data);
                this.showNotification('Real-time streaming started!', 'success');
                
                // Connect WebSocket for real-time interaction
                this.connectProjectionWebSocket(projectionId);
            } else {
                console.error('❌ Failed to start streaming:', result.message);
                this.showNotification('Failed to start streaming', 'error');
            }
        } catch (error) {
            console.error('❌ Error starting streaming:', error);
            this.showNotification('Error starting streaming', 'error');
        }
    }
    
    async enableCollaborativeMode() {
        try {
            const projectionId = this.getSelectedProjectionId();
            if (!projectionId) {
                alert('Please select a projection first');
                return;
            }
            
            // Get current participants (simulated)
            const participants = ['user_1', 'user_2', 'user_3'];
            
            const response = await fetch(`/api/v1/holographic/projections/${projectionId}/collaborative`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(participants)
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('👥 Collaborative mode enabled:', result.data);
                this.showNotification('Collaborative mode enabled!', 'success');
            } else {
                console.error('❌ Failed to enable collaborative mode:', result.message);
                this.showNotification('Failed to enable collaborative mode', 'error');
            }
        } catch (error) {
            console.error('❌ Error enabling collaborative mode:', error);
            this.showNotification('Error enabling collaborative mode', 'error');
        }
    }
    
    async activateScenario(scenarioId) {
        try {
            const scenarioConfig = {
                elements: [
                    {
                        device_id: 'holo_proj_001',
                        type: 'interactive_3d',
                        model_url: '/models/scenario_' + scenarioId + '.gltf',
                        position: [0.0, 0.0, 0.0],
                        rotation: [0.0, 0.0, 0.0],
                        scale: 1.0,
                        is_interactive: true
                    }
                ]
            };
            
            const response = await fetch(`/api/v1/holographic/scenarios/${scenarioId}/activate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(scenarioConfig)
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('🚀 Scenario activated:', result.data);
                this.currentScenario = scenarioId;
                this.activeProjections.push(...result.data.projection_ids);
                this.updateProjectionDisplay();
                this.updateStatus();
                this.showNotification(`Scenario '${result.data.scenario_name}' activated!`, 'success');
            } else {
                console.error('❌ Failed to activate scenario:', result.message);
                this.showNotification('Failed to activate scenario', 'error');
            }
        } catch (error) {
            console.error('❌ Error activating scenario:', error);
            this.showNotification('Error activating scenario', 'error');
        }
    }
    
    connectProjectionWebSocket(projectionId) {
        try {
            const ws = new WebSocket(`ws://${window.location.host}/api/v1/holographic/ws/${projectionId}`);
            
            ws.onopen = () => {
                console.log(`🔮 WebSocket connected for projection: ${projectionId}`);
                this.websocketConnections[projectionId] = ws;
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleProjectionUpdate(projectionId, data);
            };
            
            ws.onclose = () => {
                console.log(`🔮 WebSocket disconnected for projection: ${projectionId}`);
                delete this.websocketConnections[projectionId];
            };
            
            ws.onerror = (error) => {
                console.error(`❌ WebSocket error for projection ${projectionId}:`, error);
            };
        } catch (error) {
            console.error('❌ Error connecting WebSocket:', error);
        }
    }
    
    handleProjectionUpdate(projectionId, data) {
        console.log(`🔮 Projection update for ${projectionId}:`, data);
        
        // Update projection display
        this.updateProjectionDisplay();
        
        // Trigger 3D visualization update if available
        if (window.seeker3DEcosystem && window.seeker3DEcosystem.updateProjection) {
            window.seeker3DEcosystem.updateProjection(projectionId, data);
        }
    }
    
    updateProjectionDisplay() {
        const projectionList = document.getElementById('projection-list');
        
        projectionList.innerHTML = this.activeProjections.map(projection => `
            <div class="projection-item">
                <div class="projection-header">
                    <span class="projection-id">${projection.projection_id || projection}</span>
                    <span class="projection-type">${projection.projection_type || 'Unknown'}</span>
                </div>
                <div class="projection-actions">
                    <button class="btn btn-sm btn-info" onclick="holographicProjection.viewProjection('${projection.projection_id || projection}')">
                        👁️ View
                    </button>
                    <button class="btn btn-sm btn-warning" onclick="holographicProjection.updateProjection('${projection.projection_id || projection}')">
                        ✏️ Edit
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="holographicProjection.removeProjection('${projection.projection_id || projection}')">
                        🗑️ Remove
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    getSelectedProjectionId() {
        // For now, return the first active projection
        return this.activeProjections.length > 0 ? this.activeProjections[0] : null;
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
    
    // Public methods for external access
    async getDeviceStatus(deviceId) {
        try {
            const response = await fetch(`/api/v1/holographic/devices/${deviceId}`);
            const result = await response.json();
            
            if (result.success) {
                console.log('📊 Device status:', result.data.device);
                this.showNotification(`Device status: ${result.data.device.is_active ? 'Active' : 'Inactive'}`, 'info');
            } else {
                console.error('❌ Failed to get device status:', result.message);
            }
        } catch (error) {
            console.error('❌ Error getting device status:', error);
        }
    }
    
    viewScenarioDetails(scenarioId) {
        const scenario = this.businessScenarios.find(s => s.id === scenarioId);
        if (scenario) {
            alert(`Scenario: ${scenario.name}\n\nDescription: ${scenario.description}\n\nUse Cases:\n${scenario.use_cases.join('\n')}`);
        }
    }
    
    viewProjection(projectionId) {
        console.log(`👁️ Viewing projection: ${projectionId}`);
        this.showNotification(`Viewing projection: ${projectionId}`, 'info');
    }
    
    updateProjection(projectionId) {
        console.log(`✏️ Updating projection: ${projectionId}`);
        this.showNotification(`Updating projection: ${projectionId}`, 'info');
    }
    
    async removeProjection(projectionId) {
        try {
            const response = await fetch(`/api/v1/holographic/projections/${projectionId}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.success) {
                console.log('🗑️ Projection removed:', projectionId);
                this.activeProjections = this.activeProjections.filter(p => p !== projectionId);
                this.updateProjectionDisplay();
                this.updateStatus();
                this.showNotification('Projection removed successfully!', 'success');
            } else {
                console.error('❌ Failed to remove projection:', result.message);
                this.showNotification('Failed to remove projection', 'error');
            }
        } catch (error) {
            console.error('❌ Error removing projection:', error);
            this.showNotification('Error removing projection', 'error');
        }
    }
}

// Initialize holographic projection when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.holographicProjection = new SEEKERHolographicProjection();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SEEKERHolographicProjection;
} 
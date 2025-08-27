# SEEKER Device - Fusion 360 Quick Reference Card
## Essential Commands & Shortcuts for Beginners

---

## 🎯 **Essential Keyboard Shortcuts**

| Command | Shortcut | Description |
|---------|----------|-------------|
| **Sketch** | `S` | Create new sketch |
| **Extrude** | `E` | Extrude selected geometry |
| **Revolve** | `R` | Revolve around axis |
| **Fillet** | `F` | Add rounded corners |
| **Chamfer** | `C` | Add angled corners |
| **Hole** | `H` | Create holes |
| **Pattern** | `P` | Create patterns |
| **Mirror** | `M` | Mirror geometry |
| **Offset** | `O` | Offset geometry |
| **Trim** | `T` | Trim geometry |
| **Extend** | `X` | Extend geometry |
| **Undo** | `Ctrl+Z` | Undo last action |
| **Redo** | `Ctrl+Y` | Redo last action |
| **Save** | `Ctrl+S` | Save design |
| **Zoom** | `Mouse Wheel` | Zoom in/out |
| **Pan** | `Shift+Mouse` | Pan view |
| **Rotate** | `Ctrl+Mouse` | Rotate view |

---

## 📐 **Sketch Tools**

### **Basic Shapes**
- **Rectangle**: `R` - Draw rectangles
- **Circle**: `C` - Draw circles
- **Line**: `L` - Draw lines
- **Arc**: `A` - Draw arcs
- **Polygon**: `P` - Draw polygons

### **Modify Tools**
- **Fillet**: `F` - Round corners
- **Chamfer**: `C` - Angle corners
- **Trim**: `T` - Remove geometry
- **Extend**: `X` - Extend geometry
- **Offset**: `O` - Offset geometry

### **Pattern Tools**
- **Rectangular Pattern**: Create grid patterns
- **Circular Pattern**: Create circular patterns
- **Mirror**: Mirror geometry
- **Copy**: Copy geometry

---

## 🔧 **Model Tools**

### **Create Tools**
- **Extrude**: `E` - Extrude sketches
- **Revolve**: `R` - Revolve around axis
- **Sweep**: `S` - Sweep along path
- **Loft**: `L` - Loft between profiles
- **Hole**: `H` - Create holes

### **Modify Tools**
- **Fillet**: `F` - Round edges
- **Chamfer**: `C` - Angle edges
- **Shell**: `S` - Create hollow parts
- **Draft**: `D` - Add draft angles
- **Split**: `S` - Split bodies

### **Pattern Tools**
- **Rectangular Pattern**: Pattern in grid
- **Circular Pattern**: Pattern in circle
- **Mirror**: Mirror bodies
- **Copy**: Copy bodies

---

## 🎨 **SEEKER Device Specific Commands**

### **Housing Creation**
```fusion360
1. Sketch → Rectangle (145×80mm)
2. Extrude → 28mm height
3. Fillet → 8mm corner radius
4. Shell → 2mm wall thickness
```

### **Component Mounting**
```fusion360
1. Sketch → Offset (5mm from edges)
2. Extrude → 2mm mounting plate
3. Hole → 3mm mounting holes
4. Pattern → 4×4 hole array
```

### **Port Creation**
```fusion360
1. Sketch → Rectangle (8.5×3mm)
2. Extrude Cut → Through all
3. Fillet → 0.5mm corner radius
4. Chamfer → 0.3mm edge chamfer
```

### **Battery Compartment**
```fusion360
1. Sketch → Rectangle (45×60mm)
2. Extrude Cut → 1.5mm depth
3. Fillet → 2mm corner radius
4. Pattern → 2×2 cell array
```

---

## 🔌 **Assembly Commands**

### **Joint Creation**
- **Fixed Joint**: `J` - Fix component in place
- **Rigid Joint**: `R` - Rigid connection
- **Revolute Joint**: `R` - Rotating connection
- **Slider Joint**: `S` - Sliding connection

### **Component Management**
- **New Component**: Right-click → New Component
- **Activate Component**: Double-click component
- **Insert Component**: Insert → Insert into Design
- **Move Component**: Move/Copy tool

### **Assembly Tools**
- **Joint**: `J` - Create joints
- **Contact**: `C` - Set contact relationships
- **Interference**: `I` - Check interference
- **Exploded View**: `E` - Create exploded view

---

## 🏭 **Manufacturing Commands**

### **Draft Angles**
```fusion360
1. Select faces
2. Modify → Draft
3. Set angle: 2°
4. Set direction: +Z
```

### **Ejection Pins**
```fusion360
1. Sketch → Circle (4mm diameter)
2. Extrude Cut → 2mm depth
3. Pattern → 4×3 array
4. Draft → 1° angle
```

### **Parting Line**
```fusion360
1. Sketch → Line at mid-height
2. Extrude → Create separation
3. Add alignment pins
4. Add venting channels
```

---

## 📐 **Drawing Commands**

### **Create Views**
- **Base View**: `B` - Create base view
- **Projected View**: `P` - Project from base
- **Section View**: `S` - Create section
- **Detail View**: `D` - Create detail

### **Add Dimensions**
- **Linear Dimension**: `L` - Linear measurements
- **Angular Dimension**: `A` - Angular measurements
- **Radius Dimension**: `R` - Radius measurements
- **Diameter Dimension**: `D` - Diameter measurements

### **Add Annotations**
- **Text**: `T` - Add text notes
- **Leader**: `L` - Add leaders
- **Table**: `T` - Create tables
- **Balloon**: `B` - Add balloons

---

## 🎯 **SEEKER Device Dimensions**

### **Main Housing**
- **Overall**: 145×80×28mm
- **Wall Thickness**: 2mm
- **Corner Radius**: 8mm
- **Draft Angle**: 2°

### **Internal Components**
- **Snapdragon**: 25×25×2mm
- **NPU**: 20×20×3mm
- **Battery**: 45×60×8mm
- **PCB**: 130×70×1.6mm

### **Connectors**
- **USB-C**: 8.5×3×4mm
- **Power Button**: 6×6×3mm
- **Microphones**: 2mm diameter
- **Camera**: 12×8×6mm

---

## 🔧 **Troubleshooting Commands**

### **Fix Common Issues**
- **Check Interference**: Inspect → Interference
- **Measure Distance**: Inspect → Measure
- **Check Mass Properties**: Inspect → Mass Properties
- **Validate Design**: Inspect → Validate Design

### **Repair Geometry**
- **Stitch**: Surface → Stitch
- **Heal**: Surface → Heal
- **Fill**: Surface → Fill
- **Trim**: Surface → Trim

---

## 📋 **Project Workflow**

### **Phase 1: Basic Shapes**
1. Create main housing
2. Add corner fillets
3. Create mounting plate
4. Add component areas

### **Phase 2: Details**
1. Add ports and connectors
2. Create ventilation holes
3. Add speaker grilles
4. Create camera module

### **Phase 3: Components**
1. Create individual components
2. Position in assembly
3. Create joints
4. Check interference

### **Phase 4: Manufacturing**
1. Add draft angles
2. Create parting lines
3. Add ejection pins
4. Generate drawings

---

## 🎓 **Beginner Tips**

1. **Save Often**: Ctrl+S every 10 minutes
2. **Use Undo**: Ctrl+Z for mistakes
3. **Check Dimensions**: Always verify measurements
4. **Test Assembly**: Move components to check fit
5. **Use Patterns**: Save time with patterns
6. **Add Fillets**: Improve manufacturability
7. **Check Interference**: Avoid overlapping parts
8. **Use Components**: Organize your design

This quick reference card will help you navigate Fusion 360 efficiently while modeling the SEEKER device! 
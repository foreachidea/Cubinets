# [ ]]] Cubinets 

Cubinets is a FreeCAD Workbench for furniture makers, developed to simplify and accelerate the design and production process. Visualise Cabinet Assemblies in minutes using Parametric Templates and Generate Cut Lists instantly.

![demo](https://img.shields.io/badge/version-v0.1.0--demo-green)


## 🔥Concept Demo

https://vyt4ut4s.github.io/media/Cubinets/concept_demo.mp4

## 🔥Parametric Template design Demo

** demo gif **


# 🛠️ Installation

- ✅ Install FreeCAD from the official website - ![FreeCAD](https://www.freecad.org)
- ✅ Download Cubinets latest release - ![Latest Release](https://github.com/vyt4ut4s/Cubinets/releases/latest)
- ✅ Extract archive contents to FreeCAD workbenches folder:
  - 🍎 On **macOS** it is usually /Applications/FreeCAD/Mod/
  - 🪟 On **Windows** it is usually C:\Program Files\FreeCAD\Mod\
  - 🐧 On **Linux** it is usually /usr/share/freecad/Mod/
    - For snap versions (for instance on Ubuntu) it is $HOME/snap/freecad/common/Mod/


# 👨‍💻 Usage

**video: how to use**
**video: how to design a parametric template**

## Directives
| directive | description |
|---|---|
| `void` | creates a void in the assembly of a certain width; eg.: space for a cooker, fireplace, dreams and imagination, etc. |
| empty row | indicates a new row of cabinet units; *currently, only 2 rows supported* |


## Provided Templates

| Name| Description |
|---|---|
| `cubinet` | one door cabinet |
| `cubinet double` | two door cabinet |
| `cubinet drawer` | one door cabinet with a drawer |

> [!TIP]
> Users are welcome to Design and use their own Parametric Templates.


## Parameters

| Name | | | | | | | | | | | |
|-|-|-|-|-|-|-|-|-|-|-|-|
| `void` | width |
| `cubinet` | unit width | unit height | unit depth | material thickness | door margin |
| `cubinet double` | unit width | unit height | unit depth | material thickness | door margin |
| `cubinet drawer` | unit width | unit height | unit depth | material thickness | door margin | top panel depth (%) | drawer face height | drawer box height | drawer box bottom margin | drawer box material thickness | drawer box rail width |

> [!NOTE]
> Parameters provided in millimeters, unless stated otherwise.
> eg.: cubinet drawer - top panel depth (%)


## Example Kitchen Assembly

This example contains handfull of cabinets and voids for the boiler, extractor and cooker.

copy/paste these values to a "params" spreadsheet and click Assemble.


```
void	400										
cubinet	400	700	300	18	2						
void	600										
cubinet double	800	700	300	18	2						
cubinet	400	700	300	18	2						
											
cubinet drawer	400	700	300	18	2	20	140	100	10	10	20
cubinet drawer	400	700	300	18	2	20	140	100	10	10	20
void	600										
cubinet drawer	400	700	300	18	2	20	140	100	10	10	20
cubinet drawer	400	700	300	18	2	20	140	100	10	10	20
cubinet drawer	400	700	300	18	2	20	140	100	10	10	20
```

<img src="https://vyt4ut4s.github.io/media/Cubinets/example_kitchen_assembly.jpg" alt="example kitchen assembly" width="40%">

I know what yer thinking: finally some units with realistic parameters. Enjoy!


## Template Design Protocol

- 📌 Template must contain a "params" spreadsheet
- 📌 Spreadsheet format
  - 📌 Column A - parameter name, eg.: unit width, material thickness, etc.
  - 📌 Column B - value (default), eg.: 140, 600, etc. 
  - 📌 Column C - value unit description, eg.: mm, %
  - 📌 Use of other Columns is unconstrained - user is free to use it (or not) for notes, calculations, etc.
- 📌 All parts must be a Cube from Part Workbench; In technical terms - Part_Box.
- 📌 XY plane (top view - table saw/CNC perspective) must be used to design parts.

*more info comming soon..*


# 🎯 Roadmap

## ✅ Current Version (v0.1.0-demo)
- ✅ Visualise Cabinet Assemblies using Parametric Templates
- ✅ Generate Part Cutlist


### 🔄 Upcoming (v1.0)
- 🔄 Complete code rewrite: spagetti to a readable, scaleable and extendible code
- 🔄 UX/UI Improvments - Settings Dialog, Parameter Hints, ...
- 🔄 New App Features
- 🔄 New Template Features - count objects, eg.: shelves
- 🔄 New Templates


### 💡 Ideas
- 💡 Quality Visual Renderings
- 💡 CNC automation


## ❤️ Donate

### 🌱 Help this project grow
 - ☕ If you like this sofware, buy me a coffee.
 - 🧩 If you find it usefull in your proffesional activities, consider donating a larger sum. 

**donate button**


## 📝 License

This project is licensed under the **GPL-3.0 License**, see [LICENSE](./LICENSE.txt).

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![PySide2](https://img.shields.io/badge/PySide2-5.15%2B-green)](https://wiki.qt.io/PySide2)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![LGPL Dependencies](https://img.shields.io/badge/Dependencies-LGPL--3.0-orange)](./LICENSES/LGPL-3.0.txt)
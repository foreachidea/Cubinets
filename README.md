# [ ]]] Cubinets 

Cubinets is a FreeCAD Workbench for furniture makers, developed to simplify and accelerate the design and production process. Visualise Cabinet Assemblies in minutes, using Parametric Templates and Generate Cut Lists instantly.


## 🔥Concept Demo

![concept demo](https://vyt4ut4s.github.io/media/Cubinets/concept_demo.gif)

<video src="https://vyt4ut4s.github.io/media/Cubinets/concept_demo.mp4"
       autoplay
       loop
       muted
       playsinline>
</video>

<img src="https://vyt4ut4s.github.io/media/Cubinets/concept_demo.gif" alt="Alt text">


## 🔥Parametric Template design Demo

** demo gif **


# 🛠️ Installation

- ✅ Install FreeCAD from the official website - https://www.freecad.org
- ✅ Download Cubinets latest release - https://github.com/vyt4ut4s/Cubinets/releases/latest
- ✅ Extract archive contents to FreeCAD workbenches folder:
  - On **macOS** it is usually /Applications/FreeCAD/Mod/
  - On **Windows** it is usually C:\Program Files\FreeCAD\Mod\
  - On **Linux** it is usually /usr/share/freecad/Mod/
    - For snap versions (for instance on Ubuntu) it is $HOME/snap/freecad/common/Mod/


# 👨‍💻 Usage

**video: how to use**
**video: how to design a parametric template**

## Directives
| directive | description |
|---|---|
| `void` | creates a void in the assembly of a certain width; eg.: space for a cooker, fireplace, dreams and imagination, etc. |
| empty row | indicates a new row of units; currently only 2 rows implemented. |


## Provided Templates

| Name| Description |
|---|---|
| `cubinet` | one door cabinet |
| `cubinet double` | two door cabinet |
| `cubinet drawer` | one door cabinet with a drawer |

> [!TIP]
> Users are welcome to Design and use own Parametric Templates.


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

copy/paste these values to a "params" spreadsheet and click Assemble 

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


## Template Design Conventions

**conventions**


# 🎯 Roadmap

## ✅ Current Version (v0.1.0-demo)
- ✅ Visualise Cabinet Assemblies using pre-designed Parametric Templates
- ✅ Generate Part Cutlist


### 🔄 Upcoming (v1.0)
- 🔄 Complete code rewrite: spagetti to a readable, scaleable and extendible code
- 🔄 User Experience and User Interface improvments;
- 🔄 New App features
- 🔄 New Template features
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

This project is licensed under the **GPL-3.0 License**, see [LICENSE](./LICENSE).

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![PySide2](https://img.shields.io/badge/PySide2-5.15%2B-green)](https://wiki.qt.io/PySide2)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![LGPL Dependencies](https://img.shields.io/badge/Dependencies-LGPL--3.0-orange)](./LICENSES/)
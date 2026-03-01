# [ ]]] Cubinets

## 🥥 In a nutshell

Cubinets is a FreeCAD Workbench for furniture makers, developed to simplify and accelerate design and production process. Using Parametric Templates visualise Cabinet Assemblies in minutes and Generate Cut Lists instantly.

![demo](https://img.shields.io/badge/version-v0.1.0--demo-green)


## 💡 Tell me more...

Designing Cabinet Assemblies (i.e. Kitchen) is a repetative business. You take meassurements of the room, plan the position of your appliances, select cabinet style and materials. Then produce a design and present it to client, revise, redisign, prepare cutlist and start the production...

What if you could visualise the end result right after meassuring the room? On site. In minutes!


## 🔥Concept Demo

https://vyt4ut4s.github.io/media/Cubinets/concept_demo.mp4


# 🛠️ Installation

- ✅ Download FreeCAD from the official website - ![FreeCAD](https://www.freecad.org)
- ✅ Install FreeCAD
- ✅ Download Cubinets latest release - ![Latest Release](https://github.com/vyt4ut4s/Cubinets/releases/latest)
- ✅ Extract archive contents to FreeCAD workbenches' folder:
  - 🍎 On **macOS** it is usually /Applications/FreeCAD/Mod/
  - 🪟 On **Windows** it is usually C:\Program Files\FreeCAD\Mod\
  - 🐧 On **Linux** it is usually /usr/share/freecad/Mod/
    - For snap versions (for instance on Ubuntu) it is $HOME/snap/freecad/common/Mod/

💫 That's it!


# 👨‍💻 Usage

*video: how to use Cubinets ... coming soon*

*video: how to design a parametric templates in FreeCAD ... coming soon*

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


## Parameters of the provided Directives and Templates

| Name | | | | | | | | | | | |
|-|-|-|-|-|-|-|-|-|-|-|-|
| `void` | width |
| `cubinet` | unit width | unit height | unit depth | material thickness | door margin |
| `cubinet double` | unit width | unit height | unit depth | material thickness | door margin |
| `cubinet drawer` | unit width | unit height | unit depth | material thickness | door margin | top panel depth (%) | drawer face height | drawer box height | drawer box bottom margin | drawer box material thickness | drawer box rail width |

> [!NOTE]
> Parameters provided in millimeters, unless stated otherwise in parenthesis.
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


## 📑 Template Design Protocol (design rules)

> [!NOTE] Template document is a regular FreeCAD design document. NO added complexity.
> To create your own parametric template: open FreeCAD and create new document. That's it, you are set!

In order for Cubinets to recognise and correctly interpret your Parametric Templates, it is important to set a standart. This standart is set to be optimal practicaly and intuitive for a human person.

📌 Template document must contain a **spreadsheet named "parameters"**. This is where parameters of the *Prametric Template* will live. FreeCAD has a Spreadsheet workbench, with tools available to create and manipulate spreadsheets. However, Cubinets only require a basic spreadsheet and it is recommended to use a shortcut access - a button "New Sheet" provided in Cubinets workbench. 

📌 Spreadsheet format<br>
Column A - **parameter name**, *eg.: unit width, material thickness, etc.*<br>
Column B - **parameter value (default value)**, *eg.: 400, 700, 300, etc.*<br>
Column C - **value unit**, *eg.: mm, %, etc.*<br>
Use of other Columns is unconstrained - user is free to use it (or not) for notes, calculations, etc.

🔥 Eg.:

| | A | B | C |
|---|---|---|---|
| 1 | unit width | 400 | mm |
| 2 | unit height | 700 | mm |
| 3 | unit depth | 300 | mm |
| 4 | flex | 100 | % |

> [!IMPORTANT]
> First row parameter must be unit width. It is used to position units during the assenbly process.

> [!TIP]
> It is recommended that templates also contain unit height and unit depth parameters.

📌 **XY plane** of a 3d view  must be used to design parts. This is a top view - a perspective of a table saw or a CNC.

📌 All parts must be of a type - **Cube**, available in **Part Workbench**.

📌 Enter part dimensions in order: width, height, depth, then position and rotate it into the final desired position.

*more info comming soon..*


# 🎯 Roadmap

## ✅ Current Version (v0.1.0-demo)
- ✅ Visualise Cabinet Assemblies using Parametric Templates
- ✅ Generate Part Cutlist


## 🔄 Upcoming (v1.0)
- 🔄 Complete code rewrite: spagetti to a readable, scaleable and extendible code
- 🔄 UX/UI Improvments - Settings Dialog, Parameter Hints, ...
- 🔄 New App Features
- 🔄 New Template Features - count objects, eg.: shelves
- 🔄 New Templates


## 💡 Ideas
- 💡 Quality Visual Renderings
- 💡 CNC automation


# ❤️ Donate

## 🌱 Help this project grow
 - ☕ If you like this sofware, buy me a coffee.
 - 🧩 If you find it usefull in your professional activities, consider donating a larger sum. 

**donate button**


# 📝 License

This project is licensed under the **GPL-3.0 License**, see [LICENSE](./LICENSE.txt).

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![PySide2](https://img.shields.io/badge/PySide2-5.15%2B-green)](https://wiki.qt.io/PySide2)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![LGPL Dependencies](https://img.shields.io/badge/Dependencies-LGPL--3.0-orange)](./LICENSES/LGPL-3.0.txt)
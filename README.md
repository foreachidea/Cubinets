# [ ]]] Cubinets

## 🥥 In a nutshell

Cubinets is a FreeCAD Workbench for furniture makers, developed to simplify and accelerate design process. Using Parametric Templates, visualise Cabinet Assemblies in minutes and Generate Cut Lists instantly.

![demo](https://img.shields.io/badge/version-v0.1.0--demo-green)


## 💡 Tell me more...

Designing Cabinet Assemblies may be a repetative business. Let's say you are working on a kitchen. You arrive on site, take meassurements of the room, plan the position and space of appliances, select cabinet style and materials. Then produce a design, present it to client, revise, redesign, prepare cutlist and start the production...

What if you could visualise the end result first thing you arrive on site? In minutes!


## 🔥Concept Demo

https://foreachidea.github.io/media/Cubinets/concept_demo.mp4


## 💡 What's the idea...

While humans excel at creativity and handling ambiguity. Computers are strong in processing data quickly and accuratelly. The idea is to outsource repetitive tasks to computers, they love it!

Cabinet style is a constant - European style, shaker style, etc. Then there are variables: unit dimensions, material thikness. It makes sense to design a Parametric Template for a particular style once and reuse it over and over plugging in different values.


# 🛠️ Installation

- ✅ Download FreeCAD - ![www.freecad.org](https://www.freecad.org)<a href="https://www.freecad.org" target="_blank">www.freecad.org</a>
- ✅ Install FreeCAD
- ✅ Download Cubinets - ![Latest Release](https://github.com/foreachidea/Cubinets/releases/latest)<a href="https://github.com/vyt4ut4s/Cubinets/releases/latest" target="_blank">latest release</a>
- ✅ Extract archive contents to FreeCAD workbenches' folder:
  - 🍎 On **macOS** it is usually **/Applications/FreeCAD/Mod/**
  - 🪟 On **Windows** it is usually **C:\Program Files\FreeCAD\Mod\**
  - 🐧 On **Linux** it is usually **/usr/share/freecad/Mod/**
    - For snap versions (for instance on Ubuntu) it is **$HOME/snap/freecad/common/Mod/**

💫 That's it!


# 👨‍💻 Usage

*video: how to use Cubinets ... coming soon*

- 🧊 Open FreeCAD app
- 🧊 Create a new Document (File -> New or Ctrl + N, etc.)
- 🧊 Switch to Cubinets Workbench (View -> Workbench -> Cubinets, etc.)

- 🧊 Create a Spreadsheet (Cubinets -> New Sheet)
- 🧊 Enter data: Directives and Templates; use parameters or omit for defaults 
- 🧊 Produce Unit Assembly (Cubinets -> Assemble)
- 🧊 Produce a Cut List (Cubinets -> Cutlist)


## Directives and Provided Templates

> [!NOTE]
> Parameters provided in millimeters.

### Directives

🧊 `void`

`void` *directive* creates an empty space in the assembly of a certain width; eg.: space for a cooker, fireplace, imagination, etc.

| | |
|-|-|
| `void` | width |


🧊 empty row

empty row indicates that user finished defining the top row units and is moving on to enter data for the bottom row units; *in this demo two rows of cabinets supported*

| | |
|-|-|
|  |  |


### Provided Templates

🧊 `cubinet`

`cubinet` is a one door European style cabinet. The design has a door margin constant of 2 mm on each edge.

| | | | | |
|-|-|-|-|-|
| `cubinet` | unit width | unit height | unit depth | material thickness |


🧊 `cubinet double`

`cubinet double` is a two door European style cabinet. The design has a door margin of 2 mm on each edge.

| | | | | |
|-|-|-|-|-|
| `cubinet double` | unit width | unit height | unit depth | material thickness |


🧊 `cubinet drawer`

`cubinet drawer` is a European style cabinet with a drawer and a compartment bellow with a single door. Edge margins for the drawer face and the door are set to 2 mm on each edge. The drawer box is a full length side design, ideal to fastening with pocket screws. The back of the box is cut short for sliding in the bottom panel, into routed grooves, after the drawer box assembly. Grove depth is set to half of the drawer box material thickness. Drawer back to unit back margin set to 20 mm constant.

| | | | | |
|-|-|-|-|-|
| `cubinet drawer` | unit width | unit height | unit depth | material thickness | drawer face height | drawer box height | drawer box material thickness | drawer box rail width |


> [!TIP]
> Users are encouraged to adopt and modify exsisting or design and use their own Parametric Templates.

> [!IMPORTANT]
> Notice how some parameters are exposed as user input (eg.: unit width, material thickness) while others are built into Parametric Templates as constants (eg.: door margin: 2mm, groove depth: half of the material thickness). When designing own Parametric Templates, makers are free to decide what variables they want to expose for user entry and what they preffer to setting as constants. It is all about the balance between elegance and clutter, or rather, between being concise and verbose. These are the choices deliberated during the design process of a Parametric Template and may be unique to a maker reflecting their signature style.


### Example Kitchen Assembly

This example contains handfull of cabinets and voids for a boiler, an extractor and a cooker. Copy/paste this example to your sheet and click "Assemble".

```
void  600             
cubinet 400 700 300 18        
void  600             
cubinet double  800 500 300 18        
cubinet 400 700 300 18        
                
cubinet drawer  600 700 600 18  140 100 10  20
cubinet drawer  400 700 600 18  140 100 10  20
void  600             
cubinet drawer  400 700 600 18  140 100 10  20
cubinet drawer  400 700 600 18  140 100 10  20
cubinet drawer  400 700 600 18  140 100 10  20
```

💫 Here's the resut:

<img src="https://foreachidea.github.io/media/Cubinets/kitchen_assembly_example.jpg" alt="kitchen assembly example" width="100%">


## 📑 Template Design Protocol (design rules)

*video: how to design a Parametric Templates in FreeCAD ... coming soon*

> [!NOTE]
> Parametric Template document is a regular FreeCAD design document. NO added complexity. To create your own Parametric Template: open FreeCAD and create new document. That's it, you are set!

In order for Cubinets to recognise and correctly interpret your Parametric Templates, it is important to set a standart. This standart is aimed to be optimal practicaly and intuitive for a human person.

📌 **Parametric Template document must contain a spreadsheet named "params"**. This is short for parameters. The reason it is shortened is that this name will be used in formulas and it is a good idea too keep the formulas as short as possible. Params Spreadsheet is where parameters of the Prametric Template will live. FreeCAD has a Spreadsheet workbench, with tools available to create and manipulate spreadsheets. However, Cubinets only require a basic spreadsheet manipulation and it is recommended to use a shortcuts provided by Cubinets Workbench:
 - Toolbar button: "New Sheet"; or
 - Menu: Cubinets -> New Sheet.

📌 Spreadsheet format<br>
Column A - **parameter name**, *eg.: unit width, material thickness, etc.*<br>
Column B - **parameter value (default value)**, *eg.: 400, 700, 300, etc.*<br>
Column C - **value unit**, *eg.: mm, %, etc.*<br>
Use of other Columns is unconstrained - user is free to use it (or not) for notes, calculations, etc.

🔥 Eg.: here's the actual "cubinet double" params spreadsheet:

<img src="https://foreachidea.github.io/media/Cubinets/template_params_example1.jpg" alt="template params example" width="100%">

> [!IMPORTANT]
> Params cell B2 value **must** be a unit width! This value is used to position cabinet units during the assenbly process.

> [!TIP]
> It is recommended that templates also contain unit height and unit depth parameters. Example above satisfies this recommendation.

📌 In 3d view, switching to a **XY plane** is a **must**. This is a **top view** - a perspective of a table saw or a CNC router.

📌 All parts, or rather cabinet panels, **must** be of an object type - **Cube**, available in **Part Workbench**.

📌 Panel dimensions **must** be entered in the following order: width, height, depth. Create a panel of a desired dimensions in front of you, then position and rotate it into the final desired position.


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
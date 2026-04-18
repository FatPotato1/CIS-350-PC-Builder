"""
The purpose of this module is to define all hardware components and their prices used in the PC Builder application.

Authors: Dorian Lawton, Justin Hanko, Landon Jurmo and Jaykin Hang
Date: April 24, 2026
Version: Python 3.12
"""


# Hardware that the user will be able to choose from
hardware = {

    "NVIDIA GPUs": [
        "RTX 5090",
        "RTX 5080",
        "RTX 5070 Ti",
        "RTX 5070",
        "RTX 5060 Ti",
        "RTX 5060",
        "RTX 5050"
    ],

    "AMD GPUs": [
        "Radeon RX 9070 XT",
        "Radeon RX 9070",
        "Radeon RX 9060 XT",
        "Radeon RX 9060"
    ],

    "Intel CPUs": [
        "Core i9-14900K",
        "Core i7-14700K",
        "Core i5-14600K",
        "Core i5-14400",
        "Core i3-14100",
    ],

    "AMD CPUs": [
        "Ryzen 9 9950X",
        "Ryzen 7 9700X",
        "Ryzen 5 9600X"
    ],

    "RAM": [
        "CORSAIR VENGEANCE RGB 8GB DDR5",
        "CORSAIR VENGEANCE RGB 16GB DDR5",
        "CORSAIR VENGEANCE RGB 32GB DDR5",
        "CORSAIR VENGEANCE RGB 64GB DDR5"
    ],
    
    
    "Intel Motherboards": [
        "ASUS Prime Z790-A"
    ], 

    "AMD Motherboards": [
        "MSI B650 Tomahawk"
    ],
    
    "Cases": [
        'Montech Mid-Tower Case - Black',
        'DIYPC Wood Black Case',
        'Corsair Mid-Tower Case - White',
        'Fractal Design Meshify Case',
    ]
}


prices = {
    "NVIDIA GPUs": {
        'RTX 5090': 2000,
        'RTX 5080': 1000,
        'RTX 5070 Ti': 749,
        'RTX 5070': 550,
        'RTX 5060 Ti': 429,
        'RTX 5060': 299,
        'RTX 5050': 249
    },

    "AMD GPUs": {
        'Radeon RX 9070 XT': 599,
        'Radeon RX 9070': 549,
        'Radeon RX 9060 XT': 349,
        'Radeon RX 9060': 349,
    },

    "Intel CPUs": {
        'Core i9-14900K': 589,
        'Core i7-14700K': 409,
        'Core i5-14600K': 319,
        'Core i5-14400': 219,
        'Core i3-14100': 149
    },

    "AMD CPUs": {
        'Ryzen 9 9950X': 699,
        'Ryzen 7 9700X': 399,
        'Ryzen 5 9600X': 299
    },

    "RAM": {
        '8GB': 150,
        '16GB': 218,
        '32GB': 435,
        '64GB': 1114
    },

    "Intel Motherboards": {
        "ASUS Prime Z790-A": 300
    },

    "AMD Motherboards": {
        "MSI B650 Tomahawk": 220
    },
    
    "Cases": {
        'Montech Mid-Tower Case - Black': 70,
        'DIYPC Wood Black Case': 75,
        'Corsair Mid-Tower Case - White': 80,
        'Fractal Design Meshify Case': 154
    }

}

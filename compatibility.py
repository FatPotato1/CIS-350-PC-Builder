def is_compatible(build):
    """
    Basic compatibility check:
    - CPU brand must match motherboard brand
    """
    cpu_brand = build.get("CPU_Brand")
    motherboard = build.get("Motherboard")

    if motherboard:
        if cpu_brand == "Intel" and "Z790" not in motherboard:
            return False
        if cpu_brand == "AMD" and "B650" not in motherboard:
            return False

    return True

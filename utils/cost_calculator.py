from typing import Dict, Tuple


def compute_cost_components(inputs: Dict) -> Tuple[float, Dict[str, float]]:
    """Compute component-wise costs and total manufacturing cost.

    inputs: dictionary containing keys:
      - material_cost_per_kg
      - quantity
      - machine_hours
      - machine_rate_per_hr
      - labor_hours
      - labor_rate_per_hr
      - energy_consumption_kWh
      - energy_rate_per_kWh
      - overhead_cost
      - defect_rate (percentage, 0-100)
      - inventory_time_days
      - inventory_cost_per_day

    Returns (total_cost, breakdown_dict)
    """
    material_cost = float(inputs.get("material_cost_per_kg", 0.0)) * float(inputs.get("quantity", 0.0))
    machine_cost = float(inputs.get("machine_hours", 0.0)) * float(inputs.get("machine_rate_per_hr", 0.0))
    labor_cost = float(inputs.get("labor_hours", 0.0)) * float(inputs.get("labor_rate_per_hr", 0.0))
    energy_cost = float(inputs.get("energy_consumption_kWh", 0.0)) * float(inputs.get("energy_rate_per_kWh", 0.0))
    overhead = float(inputs.get("overhead_cost", 0.0))
    defect_loss = (float(inputs.get("defect_rate", 0.0)) / 100.0) * material_cost
    inventory_cost = float(inputs.get("inventory_time_days", 0.0)) * float(inputs.get("inventory_cost_per_day", 0.0))

    total = material_cost + machine_cost + labor_cost + energy_cost + overhead + defect_loss + inventory_cost

    breakdown = {
        "Material Cost": round(material_cost, 2),
        "Machine Cost": round(machine_cost, 2),
        "Labor Cost": round(labor_cost, 2),
        "Energy Cost": round(energy_cost, 2),
        "Overhead": round(overhead, 2),
        "Defect Loss": round(defect_loss, 2),
        "Inventory Cost": round(inventory_cost, 2),
    }

    return round(total, 2), breakdown
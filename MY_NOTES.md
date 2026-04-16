# Fleeing Behavior - Phase 1

## 1. Core Logic

To implement fleeing I need to simulate a "fear or threat" response in smaller squares when larger squares get too close

**The Plan:**

- **Detection:** Each square needs to scan the list of all other squares
- **Condition:** A square only flees if `other.size > self.size`
- **Prox:** Fleeing should only trigger within a certain radius (example 150 pixels) to prevent constant chaotic movement

# Life span + Rebirth - Phase 2

## 1. Core Logic

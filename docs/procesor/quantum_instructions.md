# Kvantové instrukce - Pearl Quantum Processor

## Přehled

Pearl Quantum Processor podporuje hybridní klasické a kvantové výpočty. Kvantové instrukce umožňují manipulaci s qubity, vytváření superpozic, provázání a měření kvantových stavů.

## Kvantové registry

### Označení qubitů:
- **q0, q1, q2, ..., qn**: kvantové registry (qubity)
- Každý qubit může být ve stavu |0⟩, |1⟩ nebo v superpozici α|0⟩ + β|1⟩
- Kvantové stavy jsou reprezentovány komplexními amplitudami

### Klasické registry pro výsledky:
- **p0-p7**: klasické registry pro ukládání výsledků měření
- **b**: boolean registr pro logické operace

---

## Jednokvbitové brány (Single-Qubit Gates)

### Základní Pauli brány:
```
x q0          # Pauli-X (kvantový NOT) - |0⟩ ↔ |1⟩
y q0          # Pauli-Y - rotace kolem Y-osy
z q0          # Pauli-Z - phase flip - |1⟩ → -|1⟩
```

### Hadamard brána:
```
h q0          # Hadamard - vytvoří superpozici
              # |0⟩ → (|0⟩ + |1⟩)/√2
              # |1⟩ → (|0⟩ - |1⟩)/√2
```

### Fázové brány:
```
s q0          # S gate - fázový posun π/2
t q0          # T gate - fázový posun π/4
sdg q0        # S† - inverzní S brána
tdg q0        # T† - inverzní T brána
```

### Rotační brány:
```
rx θ q0       # Rotace kolem X-osy o úhel θ (v radiánech)
ry θ q0       # Rotace kolem Y-osy o úhel θ
rz θ q0       # Rotace kolem Z-osy o úhel θ
p θ q0        # Fázová brána - přidá fázi e^(iθ) ke stavu |1⟩
```

---

## Dvoukvbitové brány (Two-Qubit Gates)

### Controlled brány:
```
cx q0 q1      # CNOT (Controlled-X) - pokud q0=|1⟩, aplikuje X na q1
cy q0 q1      # Controlled-Y
cz q0 q1      # Controlled-Z
ch q0 q1      # Controlled-Hadamard
cs q0 q1      # Controlled-S
ct q0 q1      # Controlled-T
```

### Swap brány:
```
swap q0 q1    # Vymění stavy qubitů q0 a q1
iswap q0 q1   # Swap s fázovým posunem i
```

---

## Tříkvbitové brány (Three-Qubit Gates)

```
ccx q0 q1 q2  # Toffoli (Controlled-Controlled-X)
              # Aplikuje X na q2, pokud q0=q1=|1⟩
cswap q0 q1 q2 # Fredkin - controlled swap
```

---

## Měření a reset

### Měření:
```
measure q0 p1    # Změří qubit q0, výsledek (0 nebo 1) uloží do registru p1
measure_all      # Změří všechny qubity najednou
```

### Reset:
```
reset q0         # Reset qubitu q0 do stavu |0⟩
reset_all        # Reset všech qubitů do |0⟩
```

---

## Kvantové pomocné instrukce

### Bariéry a synchronizace:
```
barrier q0 q1    # Kvantová bariéra - zabraňuje optimalizaci přes tuto hranici
barrier          # Bariéra pro všechny qubity
```

### Inicializace:
```
init q0 0        # Inicializuje qubit q0 do stavu |0⟩
init q0 1        # Inicializuje qubit q0 do stavu |1⟩
prep q0 θ φ      # Příprava qubitu do obecného stavu cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩
```

---

## Kvantové algoritmy (makro instrukce)

### Kvantová Fourierova transformace:
```
qft q0 q1 q2     # Aplikuje QFT na registry q0-q2
iqft q0 q1 q2    # Inverzní QFT
```

### Amplifikace amplitude:
```
diffuser q0 q1 q2 # Grover diffuser operátor
oracle q0 q1      # Oracle pro Groverův algoritmus
```

---

## Příklady kvantových programů

### 1. Vytvoření Bell state (maximálně provázaný stav):
```assembly
# Klasická příprava
reset_all
h q0          # Vytvoř superpozici na q0
cx q0 q1      # Proveď qubity q0 a q1

# Měření
measure q0 p0
measure q1 p1

# Výstup
out p0        # Vždy stejné jako p1 (00 nebo 11)
out p1
```

### 2. Kvantová teleportace:
```assembly
# Příprava provázaných qubitů
h q1
cx q1 q2

# Alice má qubit q0 k teleportaci
# Bell measurement
cx q0 q1
h q0
measure q0 p0
measure q1 p1

# Bob aplikuje korekce na q2
cmp p1 1
jmpif 15      # Pokud p1=1, aplikuj X
jmp 16
x q2          # Aplikuj X korekci

cmp p0 1
jmpif 19      # Pokud p0=1, aplikuj Z
jmp 20
z q2          # Aplikuj Z korekci

measure q2 p2 # Výsledek teleportace
out p2
```

### 3. Groverův algoritmus (hledání v databázi):
```assembly
# Inicializace - všechny qubity do superpozice
h q0
h q1
h q2

# Groverovy iterace (oracle + diffuser)
# Oracle označí hledaný prvek
cx q0 q1      # Příklad oracle pro |11⟩
ccx q0 q1 q2
cx q0 q1

# Diffuser (inversní o průměru)
h q0
h q1
x q0
x q1
cz q0 q1
x q0
x q1
h q0
h q1

# Měření
measure q0 p0
measure q1 p1
out p0
out p1
```

### 4. Kvantová superdense coding:
```assembly
# Příprava provázaného páru
h q0
cx q0 q1

# Alice kóduje 2 bity do 1 qubitu
# Pro 00: nic
# Pro 01: aplikuj Z
# Pro 10: aplikuj X  
# Pro 11: aplikuj X pak Z

mov 3 p0      # Kódujeme hodnotu 11 (binárně)
and p0        # Test bit 0
jmpif 12
jmp 13
z q0          # Aplikuj Z pro bit 0

cmp p0 2
jmpif 16
jmp 17
x q0          # Aplikuj X pro bit 1

# Bob dekóduje
cx q0 q1
h q0
measure q0 p1
measure q1 p2
out p1        # První bit
out p2        # Druhý bit
```

---

## Kvantové chyby a korekce

### Detekce chyb:
```
syndrome q0 q1 q2 a0 a1  # Syndrome extraction pro quantum error correction
correct q0 p0            # Aplikuj korekci na základě syndrome
```

---

## Simulace a ladění

### Debug instrukce:
```
print_state q0        # Vypíše aktuální kvantový stav qubitu
print_amplitudes      # Vypíše všechny amplitudy
plot_bloch q0         # Vizualizace na Blochově sféře
expectation z q0 p0   # Očekávaná hodnota Pauli-Z na qubitu q0
```

### Statistiky:
```
fidelity q0 q1 p0     # Spočítá věrnost mezi qubity
entanglement q0 q1 p0 # Míra provázání
```

---

## Poznámky k implementaci

1. **Hybridní režim**: Klasické a kvantové instrukce mohou být kombinovány v jednom programu
2. **Měření kolabuje stav**: Po měření se kvantová superpozice zhroutí na klasickou hodnotu
3. **Provázání**: Měření jednoho qubitu může ovlivnit jiný provázaný qubit
4. **Dekoherence**: V reálném světě kvantové stavy se časem degradují
5. **Simulace**: Na klasickém počítači simulujeme pouze malý počet qubitů (typicky <20)

---

## Kompatibilita s OpenQASM

Instrukce jsou navržené tak, aby byly kompatibilní s OpenQASM 3.0 standardem pro kvantové assembly jazyky.

Příklad OpenQASM kódu:
```qasm
OPENQASM 3.0;
qubit[2] q;
bit[2] c;

h q[0];
cx q[0], q[1];
c = measure q;
```

Ekvivalent v Pearl QP:
```
h q0
cx q0 q1
measure q0 p0
measure q1 p1
```

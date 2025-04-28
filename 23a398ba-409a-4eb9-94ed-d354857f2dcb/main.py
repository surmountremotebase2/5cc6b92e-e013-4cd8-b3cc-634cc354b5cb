import ta

# Assuming df already exists and has a 'close' column

# Calculate RSI for entry and exit
df['RSI_Entry'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
df['RSI_Exit'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()

# Parameters
entry_rsi_value = 35
exit_rsi_value = 35
lot_size = 2
min_bars_between = 2

# State variables
in_position = False
last_entry_index = -min_bars_between - 1
last_exit_index = -min_bars_between - 1

# Result lists
entries = []
exits = []

for i in range(1, len(df)):
    entry_signal = (
        df['RSI_Entry'].iloc[i-1] < entry_rsi_value and
        df['RSI_Entry'].iloc[i] >= entry_rsi_value and
        not in_position and
        (i > last_entry_index + min_bars_between)
    )

    exit_signal = (
        df['RSI_Exit'].iloc[i-1] > exit_rsi_value and
        df['RSI_Exit'].iloc[i] <= exit_rsi_value and
        in_position and
        (i > last_exit_index + min_bars_between)
    )

    if entry_signal:
        price = df['close'].iloc[i]
        entries.append((df.index[i], price))
        in_position = True
        last_entry_index = i

    if exit_signal:
        price = df['close'].iloc[i]
        exits.append((df.index[i], price))
        in_position = False
        last_exit_index = i

# Output results
print("Entries:", entries)
print("Exits:", exits)
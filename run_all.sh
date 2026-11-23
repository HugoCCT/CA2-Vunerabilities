#!/usr/bin/env bash
# Run each proof against both implementations and retain reproducible output.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"
classes=("01-injection" "02-idor" "03-crypto-misuse" "04-toctou")
summary=()

for class_name in "${classes[@]}"; do
  output_file="$ROOT_DIR/$class_name/test_output.txt"
  {
    printf 'Date/time: %s\n' "$(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    printf 'Python: %s\n\n' "$("$PYTHON" --version 2>&1)"
  } | tee "$output_file"

  for variant in vulnerable mitigated; do
    if [[ "$variant" == "vulnerable" ]]; then
      expected_code=0
      expected_marker='RESULT: EXPLOITED'
    else
      expected_code=1
      expected_marker='RESULT: BLOCKED'
    fi

    printf '%s\n' "--- $class_name / $variant ---" | tee -a "$output_file"
    if output=$("$PYTHON" -B "$ROOT_DIR/$class_name/exploit.py" "$variant" 2>&1); then
      actual_code=0
    else
      actual_code=$?
    fi
    printf '%s\n' "$output" | tee -a "$output_file"
    printf 'Exit code: %s\n\n' "$actual_code" | tee -a "$output_file"

    if [[ "$actual_code" -ne "$expected_code" ]] || [[ "$output" != *"$expected_marker"* ]]; then
      printf 'FAILED: %s / %s (expected exit code %s and %s)\n' \
        "$class_name" "$variant" "$expected_code" "$expected_marker" >&2
      exit 1
    fi

    summary+=("$(printf '%-18s | %-10s | %-28s | %-28s | %s' "$class_name" "$variant" "$expected_marker (exit $expected_code)" "$expected_marker (exit $actual_code)" "OK")")
  done
done

printf '\n%-18s | %-10s | %-28s | %-28s | %s\n' \
  'CLASS' 'VERSION' 'EXPECTED' 'ACTUAL' 'STATUS'
printf '%s\n' '-------------------|------------|------------------------------|------------------------------|-------'
for row in "${summary[@]}"; do
  printf '%s\n' "$row"
done

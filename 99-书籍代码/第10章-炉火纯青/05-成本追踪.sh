result=$(claude -p "review this PR" --output-format json)
cost=$(echo "$result" | jq -r '.total_cost_usd')
echo "PR_REVIEW_COST: $cost" >> /var/log/claude-costs.log

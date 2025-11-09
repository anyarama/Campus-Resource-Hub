#!/bin/bash
# Bootstrap Class Removal Script
# Removes all Bootstrap-specific classes from templates
# Run: chmod +x scripts/migrate_bootstrap_removal.sh && ./scripts/migrate_bootstrap_removal.sh

set -e

echo "🚀 Starting Bootstrap class removal..."

# Define all template files to process
FILES=(
  "src/templates/resources/detail.html"
  "src/templates/resources/create.html"
  "src/templates/resources/edit.html"
  "src/templates/resources/my_resources.html"
  "src/templates/resources/dashboard.html"
  "src/templates/resources/_resource_card.html"
  "src/templates/bookings/detail.html"
  "src/templates/bookings/my_bookings.html"
  "src/templates/bookings/new.html"
  "src/templates/bookings/_booking_card.html"
  "src/templates/admin/dashboard.html"
  "src/templates/admin/users.html"
  "src/templates/admin/user_detail.html"
  "src/templates/admin/analytics.html"
  "src/templates/auth/profile.html"
  "src/templates/concierge/index.html"
  "src/templates/concierge/help.html"
  "src/templates/reviews/_review_form.html"
  "src/templates/reviews/_review_list.html"
  "src/templates/reviews/_star_rating.html"
)

for file in "${FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "⚠️  Skipping $file (not found)"
    continue
  fi
  
  echo "📝 Processing $file..."
  
  # Create backup
  cp "$file" "${file}.bootstrap_backup"
  
  # Remove Bootstrap button classes
  sed -i '' 's/class="btn btn-outline-[a-z]*"/class="btn btn-secondary"/g' "$file"
  sed -i '' 's/ btn-sm//g' "$file"
  sed -i '' 's/ btn-lg//g' "$file"
  
  # Remove Bootstrap grid classes  
  sed -i '' 's/class="row\([^"]*\)"/class="layout-grid\1"/g' "$file"
  sed -i '' 's/class="\([^"]*\)col-md-[0-9]\([^"]*\)"/class="\1layout-col\2"/g' "$file"
  sed -i '' 's/class="\([^"]*\)col-[0-9]\([^"]*\)"/class="\1layout-col\2"/g' "$file"
  
  # Remove Bootstrap spacing utilities
  sed -i '' 's/ mb-[0-9]//g' "$file"
  sed -i '' 's/ mt-[0-9]//g' "$file"
  sed -i '' 's/ me-[0-9]//g' "$file"
  sed -i '' 's/ ms-[0-9]//g' "$file"
  sed -i '' 's/ p-[0-9]//g' "$file"
  sed -i '' 's/ py-[0-9]//g' "$file"
  sed -i '' 's/ px-[0-9]//g' "$file"
  
  # Remove Bootstrap display/flex utilities
  sed -i '' 's/ d-flex//g' "$file"
  sed -i '' 's/ d-block//g' "$file"
  sed -i '' 's/ d-inline-block//g' "$file"
  sed -i '' 's/ flex-grow-1//g' "$file"
  sed -i '' 's/ align-items-center//g' "$file"
  sed -i '' 's/ justify-content-between//g' "$file"
  sed -i '' 's/ justify-content-center//g' "$file"
  
  # Remove Bootstrap sizing
  sed -i '' 's/ w-100//g' "$file"
  sed -i '' 's/ h-100//g' "$file"
  
  # Fix badge classes (bg- prefix to badge- prefix)
  sed -i '' 's/class="\([^"]*\)badge bg-\([a-z]*\)\([^"]*\)"/class="\1badge badge-\2\3"/g' "$file"
  
  # Remove list-group classes
  sed -i '' 's/class="list-group\([^"]*\)"/class="item-list\1"/g' "$file"
  sed -i '' 's/class="list-group-item\([^"]*\)"/class="item-list-item\1"/g' "$file"
  
  # Remove Bootstrap card modifiers
  sed -i '' 's/ shadow-sm//g' "$file"
  sed -i '' 's/ border-0//g' "$file"
  sed -i '' 's/ bg-light//g' "$file"
  sed -i '' 's/ bg-white//g' "$file"
  
  # Remove Bootstrap text utilities
  sed -i '' 's/ text-muted//g' "$file"
  sed -i '' 's/ text-center//g' "$file"
  sed -i '' 's/ text-end//g' "$file"
  sed -i '' 's/ text-danger//g' "$file"
  sed -i '' 's/ text-warning//g' "$file"
  sed -i '' 's/ text-success//g' "$file"
  
  # Remove rounded utilities
  sed -i '' 's/ rounded-circle//g' "$file"
  sed -i '' 's/ rounded-pill//g' "$file"
  
  # Clean up double spaces
  sed -i '' 's/class=" /class="/g' "$file"
  sed -i '' 's/ "/"/g' "$file"
  sed -i '' 's/  / /g' "$file"
  
  echo "  ✅ Processed $file"
done

echo ""
echo "📦 Rebuilding assets..."
npm run build

echo ""
echo "🧪 Running tests..."
make test || echo "⚠️  Some tests failed (check output above)"

echo ""
echo "🔍 Running Bootstrap removal gate..."
echo "=== 1) Bootstrap CSS CDN ==="
grep -r "bootstrap.min.css" src/templates src/static 2>/dev/null || echo "✅ no-bootstrap-css"

echo ""
echo "=== 2) Bootstrap btn classes ==="
COUNT=$(grep -r 'class="btn ' src/templates/ 2>/dev/null | wc -l | tr -d ' ')
echo "Found $COUNT occurrences"
if [ "$COUNT" -eq "0" ]; then
  echo "✅ no-bootstrap-btn"
fi

echo ""
echo "=== 3) Bootstrap row classes ==="
COUNT=$(grep -r 'class="row' src/templates/ 2>/dev/null | wc -l | tr -d ' ')
echo "Found $COUNT occurrences"
if [ "$COUNT" -eq "0" ]; then
  echo "✅ no-bootstrap-grid"
fi

echo ""
echo "=== 4) Bootstrap col- classes ==="
COUNT=$(grep -r 'class="col-' src/templates/ 2>/dev/null | wc -l | tr -d ' ')
echo "Found $COUNT occurrences"
if [ "$COUNT" -eq "0" ]; then
  echo "✅ no-bootstrap-cols"
fi

echo ""
echo "✨ Migration complete! Backups saved as *.bootstrap_backup"
echo "📋 Review changes, then remove bootstrap-bridge.scss from main.scss"

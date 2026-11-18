# AssetTrack Git Branching Commands

```bash
git checkout -b feature/device-category-and-optional-serial
git add assets/models.py assets/forms.py assets/views.py assets/migrations/
git commit -m "feat: standard category dropdown, custom category field, and optional serial number"
git checkout main
git merge feature/device-category-and-optional-serial

git checkout -b feature/checkout-assign-device-redirect
git add assets/views.py templates/assets/checkout_assign.html
git commit -m "feat: redirect to device creation when no available devices exist for assignment"
git checkout main
git merge feature/checkout-assign-device-redirect

git checkout -b feature/remove-department-and-category-views
git add assets/urls.py assets/views.py templates/base.html
git commit -m "feat: eliminate department tab and redirect legacy category endpoints"
git checkout main
git merge feature/remove-department-and-category-views

git checkout -b feature/ui-dark-theme-contrast
git add static/css/theme.css templates/
git commit -m "feat: modernize high-contrast dark theme with readable bright typography"
git checkout main
git merge feature/ui-dark-theme-contrast

git checkout -b feature/company-setup-and-code
git add accounts/models.py accounts/forms.py accounts/views.py accounts/urls.py templates/accounts/company_manage.html
git commit -m "feat: admin company setup, address management, and random company code generation"
git checkout main
git merge feature/company-setup-and-code

git checkout -b feature/company-join-leave-workflow
git add accounts/models.py accounts/views.py accounts/urls.py templates/accounts/employee_company.html
git commit -m "feat: employee company join by code and admin approval workflow for join and leave"
git checkout main
git merge feature/company-join-leave-workflow

git checkout -b feature/optimistic-ui-and-toasts
git add templates/base.html templates/accounts/company_manage.html templates/accounts/employee_company.html
git commit -m "feat: instant optimistic frontend updates with right-side toast error reporting"
git checkout main
git merge feature/optimistic-ui-and-toasts

git checkout -b feature/tests-and-url-integrity
git add assets/tests.py accounts/tests.py assettrack/settings.py
git commit -m "test: comprehensive test coverage for company workflows, devices, and checkouts"
git checkout main
git merge feature/tests-and-url-integrity

git checkout -b feature/csrf-robustness-and-live-member-updates
git add assettrack/settings.py templates/base.html templates/accounts/company_manage.html templates/accounts/employee_company.html accounts/views.py accounts/urls.py accounts/tests.py
git commit -m "feat: robust csrf synchronization, live company member updates without page reload, and failure fallback"
git checkout main
git merge feature/csrf-robustness-and-live-member-updates
```

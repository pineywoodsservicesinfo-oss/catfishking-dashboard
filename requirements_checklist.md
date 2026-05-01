# Client Requirements Checklist

## Before Development Starts

### 1. Store Information

- [ ] Complete list of all 11 store locations:
  - Store name
  - Address
  - City, State, ZIP
  - Store phone number
  - Manager name
  - Manager email
  - Manager phone

- [ ] Corporate admin contacts:
  - Who needs access to the dashboard?
  - Name, email, role for each

### 2. Data Categories Priority

Rank these in order of importance (1 = most important):

- [ ] Daily sales/food cost/labor - Priority: ____
- [ ] Cash reports - Priority: ____
- [ ] Employee schedules - Priority: ____
- [ ] Payroll data - Priority: ____
- [ ] Labor projection - Priority: ____
- [ ] Food cost tracking - Priority: ____
- [ ] Invoices/purchases - Priority: ____
- [ ] Daily logs - Priority: ____
- [ ] Manager logs - Priority: ____

### 3. Historical Data Import

- [ ] What format is current year data in?
  - Excel spreadsheets?
  - CSV files?
  - POS system export?
  - Paper records?

- [ ] How many months of data to import?
  - [ ] January only
  - [ ] Q1 (Jan-Mar)
  - [ ] YTD (all of current year)
  - [ ] Previous year too?

- [ ] Who will prepare the data files?

- [ ] Data structure:
  - [ ] Single file per store
  - [ ] One combined file
  - [ ] Separate files per category

### 4. Employee & Payroll

- [ ] Approximate number of employees per store?

- [ ] Pay structure:
  - [ ] Hourly only
  - [ ] Hourly + salary
  - [ ] Hourly + tips
  - [ ] Other: ________

- [ ] Pay frequency:
  - [ ] Weekly
  - [ ] Bi-weekly
  - [ ] Semi-monthly

- [ ] Do you need the system to:
  - [ ] Calculate projected labor cost from schedule?
  - [ ] Compare projected vs actual labor?
  - [ ] Track overtime?

### 5. Inventory & Food Cost

- [ ] Current inventory tracking method:
  - [ ] Manual/spreadsheet
  - [ ] POS system
  - [ ] Vendor portal
  - [ ] Other: ________

- [ ] Primary vendors (for invoice tracking):
  - Sysco
  - US Foods
  - Ben E. Keith
  - Local suppliers
  - Other: ________

- [ ] Need inventory tracking?
  - [ ] Yes - track quantities
  - [ ] No - just costs
  - [ ] Maybe later

### 6. POS System (if applicable)

- [ ] Current POS system:
  - [ ] Square
  - [ ] Toast
  - [ ] Clover
  - [ ] Micros
  - [ ] Other: ________
  - [ ] No POS / Manual

- [ ] Interest in POS integration?
  - [ ] Yes - would like automatic sales import
  - [ ] No - manual entry is fine
  - [ ] Maybe in the future

### 7. Reporting Needs

What reports does corporate need to see?

- [ ] Daily sales summary
- [ ] Weekly comparison (store vs store)
- [ ] Monthly P&L by store
- [ ] Labor cost percentage
- [ ] Food cost percentage
- [ ] Year-over-year comparison
- [ ] Custom reports: ________

### 8. User Access & Permissions

- [ ] Who can view all stores?
  - [ ] Corporate only
  - [ ] District managers
  - [ ] All managers

- [ ] Who can edit data?
  - [ ] Only their store
  - [ ] District managers can edit their stores
  - [ ] Corporate can edit all

- [ ] Who can add employees?
  - [ ] Store managers
  - [ ] Corporate only
  - [ ] HR department

### 9. Branding & Design

- [ ] Logo file (PNG/SVG)

- [ ] Brand colors:
  - Primary: ________
  - Secondary: ________

- [ ] Tagline/slogan: ________

- [ ] Any design preferences?
  - [ ] Match current website
  - [ ] Match restaurant decor
  - [ ] Professional/corporate
  - [ ] Modern/tech-forward

### 10. Timeline & Deployment

- [ ] Ideal launch date: ________

- [ ] Training needs:
  - [ ] In-person training at corporate office
  - [ ] Video call walkthrough
  - [ ] Written documentation only
  - [ ] Pre-recorded video tutorials

- [ ] Rollout preference:
  - [ ] All stores at once
  - [ ] Pilot 2-3 stores first
  - [ ] Corporate dashboard first, stores second

### 11. Technical & Security

- [ ] IT contact for questions: ________

- [ ] Security requirements:
  - [ ] Standard (password protected)
  - [ ] 2-factor authentication required
  - [ ] SSO integration needed
  - [ ] Other: ________

- [ ] Data residency requirements:
  - [ ] US servers only
  - [ ] No restrictions
  - [ ] Other: ________

- [ ] Need to keep data after contract ends?
  - [ ] Yes - provide export
  - [ ] No - can delete
  - [ ] TBD

---

## Data Format Examples (Ask Client to Provide)

Please provide sample files for:

1. **Daily sales data** - How do you currently track daily sales?
2. **Employee list** - Employee name, position, hourly rate
3. **Schedule format** - Weekly schedule example
4. **Invoice example** - Vendor invoice or purchase record
5. **Cash report** - Current cash reconciliation sheet

---

## Questions to Ask Chris (Quick List)

1. "What's your ideal launch date?"
2. "Who will be entering data daily - managers or someone else?"
3. "Do you want POS integration or is manual entry fine?"
4. "How many months of historical data do you need imported?"
5. "Who should have admin access vs manager access?"
6. "Do you track inventory quantities or just costs?"
7. "What reports are most critical for corporate to see weekly?"
8. "Is there an IT person I should coordinate with?"
9. "Do you need in-person training or is remote okay?"
10. "Any specific security requirements (2FA, etc.)?"
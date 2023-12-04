function Yorai-Levi {
    <#
    .SYNOPSIS
    Mitigate challenges through software.
    .LINK
    resume.yorailevi.com
    .LINK
    pdf.resume.yorailevi.com
    #>
    [CmdletBinding(PositionalBinding = $false, SupportsShouldProcess = $false, DefaultParameterSetName = 'Default', HelpURI='https://resume.yorailevi.com')]
    param (
        [Parameter(Mandatory = $false, Position = 0, ParameterSetName = 'Experience')]
        [datetime]$FromDate,
        [Parameter(Mandatory = $false, Position = 1, ParameterSetName = 'Experience')]
        [datetime]$ToDate,
        [Parameter(Mandatory = $false, ParameterSetName = 'Experience')]
        [switch]$Experience,
        [Parameter(Mandatory = $false, ParameterSetName = 'Contact')]
        [switch]$Contact,
        [Parameter(Mandatory = $false, ParameterSetName = 'Contact')]
        [string]$Phone,
        [Parameter(Mandatory = $false, ParameterSetName = 'Contact')]
        [string]$Email,
        [Parameter(Mandatory = $false, ParameterSetName = 'Contact')]
        [string[]]$Location,
        [Parameter(Mandatory = $false, ParameterSetName = 'AwardsAndEducation')]
        [switch]$AwardsAndEducation
        # [Parameter(Mandatory = $false, ParameterSetName = 'Contact')]
        # [switch]$Contact,
        # [Parameter(Mandatory = $false, ParameterSetName = 'Contact')]
        # [string]$Phone = '+972-525602337',
        # [Parameter(Mandatory = $false, ParameterSetName = 'Contact')]
        # [string]$Email = 'contact@yorailevi.com',

        # [ValidateSet('Full Time', 'Part Time')]
        # [Parameter(Mandatory = $false, ParameterSetName = 'Contact')]
        # [string]$EmploymentType = 'Full Time',
        # [ValidateSet('Israel', 'Remote')]
        # [Parameter(Mandatory = $false, ParameterSetName = 'Contact')]
        # [string]$Location,
        # [ValidateSet('English', 'Hebrew')]
        # [Parameter(Mandatory = $false, ParameterSetName = 'Contact')]
        # [string[]]$Languages,
        # [Parameter(Mandatory = $false, ParameterSetName = 'AwardsAndEducation')]
        # [switch]$AwardsAndEducation = $true,
        # [Parameter(Mandatory = $false, Position = 0, ParameterSetName = 'Default')]
        # [datetime]$FromDate,
        # [Parameter(Mandatory = $false, Position = 1, ParameterSetName = 'Default')]
        # [datetime]$ToDate
    )
    $FromDate = $FromDate ?? ([datetime]::MinValue)
    $ToDate = $ToDate ?? ([datetime]::MaxValue)

    $_experience = @(
        @{
            AwardsAndEducation = 'Education'
            Title              = 'B.Sc. Mathematics with Statistics and Operations Research'
            Company            = 'Technion'
            Accomplishments    = 'Extra curriculum in deep machine learning and natural language processing (NLP)'
            FromDate           = (Get-Date -Month 10 -Year 2018)
            ToDate             = (Get-Date -Month 10 -Year 2023)
        },
        @{
            AwardsAndEducation = 'Education'
            Title              = 'Curious Learner'
            Company            = 'Actively pursuing ongoing education through platforms like MIT OpenCourseWare, edX, Coursera, Udemy, Youtube, etc.'
            Accomplishments    = 'Focused on improving skills in Data Science, Mathematics, Physics, Statistics, Software Engineering, DevOps, Cloud Computing, and more.'
            FromDate           = [datetime]::MinValue
            ToDate             = [datetime]::MaxValue
        },
        @{
            AwardsAndEducation = 'Award'
            Title              = 'Belkin Energy Disaggregation Competition'
            Company            = 'Kaggle'
            Accomplishments    = 'Achieved 3rd place, winning $2500'
            Duties             = 'Supervised electrical data analysis, classifying the electrical state of non-smart appliances through time based on grid data.'
            Technologies       = @('Matlab')
            FromDate           = (Get-Date -Month 7 -Year 2013)
            ToDate             = (Get-Date -Month 10 -Year 2013)
        },
        @{
            Title        = 'IT specialist'
            Company      = 'Axiom Computers (self employed)'
            Duties       = @('Efficient diagnosis and resolution of software and hardware mishaps and malfunctions', 'General IT support and asisstance')
            Technologies = @('Knowledge in consumer hardware', 'Windows', 'Linux')
            FromDate     = (Get-Date -Month 7 -Year 2015)
            ToDate       = (Get-Date -Month 9 -Year 2017)
        },
        @{
            Title           = 'IT specialist'
            Company         = 'Intel'
            EmploymentType  = 'Temporary project'
            Duties          = @('QA automation scripts', 'General lab support and asisstance')
            Technologies    = @('Python', 'Linux', 'Redhat')
            Accomplishments = 'Delivered tooling and technical support for dynamic and evolving projects using Python and Linux.'
            FromDate        = (Get-Date -Month 10 -Year 2016)
            ToDate          = (Get-Date -Month 4 -Year 2017)
        },
        @{
            Title    = 'Personal & Group Tutor'
            Company  = 'Technion & Nachshon Project'
            Duties   = @('Expert tutoring in mathematics and physics for Technion pre-university and high school students.')
            FromDate = (Get-Date -Month 10 -Year 2020)
            ToDate   = (Get-Date -Month 6 -Year 2021)
        },
        @{
            Title           = 'Software Engineer'
            Company         = 'Sanolla - AI Powered Primary Care Diagnostic Solutions (Startup)'
            Duties          = @('Spearhead development of companion apps for embedded devices, contributing to diagnostic solutions.')
            Technologies    = @('C', 'Android', 'Java', 'Kotlin', 'React', 'React Native', 'C#', 'WPF', 'Python', 'PowerShell', 'Bash', 'Matlab', 'AI technologies')
            Accomplishments = @('Lead tooling and quality assurance efforts for R&D and seamless UI/UX experience.')
            FromDate        = (Get-Date -Month 6 -Year 2021)
            ToDate          = ([datetime]::Today)
        }
    )
    if ($PSCmdlet.ShouldProcess('Your product', 'Innovate')) {
        switch ($PSCmdlet.ParameterSetName) {
            'AwardsAndEducation' {
                $learning = $_experience | Where-Object { $_.AwardsAndEducation }
                $learning | Sort-Object -Property FromDate -Descending | ForEach-Object {
                    $_FromDate = $(Get-Date -Date $_.FromDate -UFormat '%b %y')
                    $_ToDate = $(Get-Date -Date $_.ToDate -UFormat '%b %y')
                    $_ToDate = "- $_ToDate"
                    "$($_.Company). $($_.EmploymentType)"
                    "$($_.Title) | $_FromDate $_ToDate"
                    if (-not [string]::IsNullOrEmpty($_.Accomplishments)) { "    $($_.Accomplishments)" }
                    if (-not [string]::IsNullOrEmpty($_.Duties)) { "    $($_.Duties)" }
                    if (-not [string]::IsNullOrEmpty($_.Technologies)) { "    Proficiency: $($_.Technologies)" }
                    ''
                }
            }
            'Experience' {
                $jobs = $_experience | Where-Object { -not $_.AwardsAndEducation }
                $jobs | Where-Object { $FromDate -le $_.FromDate.AddDays(1) -and $_.ToDate.AddDays(-1) -le $ToDate } | Sort-Object -Property FromDate -Descending | ForEach-Object {
                    $_FromDate = $(Get-Date -Date $_.FromDate -UFormat '%b %y')
                    $_ToDate = if ($_.ToDate -eq [datetime]::Today) { 'Present' } else { $(Get-Date -Date $_.ToDate -UFormat '%b %y') }
                    "$($_.Company). $($_.EmploymentType)"
                    "$($_.Title) | $_FromDate - $_ToDate"
                    if (-not [string]::IsNullOrEmpty($_.Accomplishments)) { "    $($_.Accomplishments)" }
                    if (-not [string]::IsNullOrEmpty($_.Duties)) { "    $($_.Duties)" }
                    if (-not [string]::IsNullOrEmpty($_.Technologies)) { "    Proficiency: $($_.Technologies)" }
                    ''
                }
            }
            'Contact' {

            }
        }
    }
    else {
        'What if: Performing the operation "Innovate" on target "Your product".'
    }
}
function Resume-YoraiLevi {
    $Keywords = @(
        'ai',
        'ansible',
        'arduino',
        'automation',
        'bash',
        'big data',
        'c',
        'c#',
        'c++',
        'cloud computing',
        'crawling',
        'data science',
        'deployment',
        'develop',
        'devops',
        'embedded',
        'java',
        'javascript',
        'kotlin',
        'linux',
        'mathematics',
        'matlab',
        'optimization',
        'physics',
        'powershell',
        'puppeteer extra stealth',
        'puppeteer',
        'python',
        'react native',
        'react',
        'redhat',
        'software engineering'
        'statistics',
        'tools',
        'typescript',
        'web',
        'windows',
        'wpf',
        'wsl2'
    )
    $examples = @(
        { Yorai-Levi -Contact -Phone '+972-525602337' -Email 'contact@yorailevi.com' -Location 'Israel', 'Remote'}
        { Yorai-Levi -Experience },
        { Yorai-Levi -AwardsAndEducation }
    )
    'PS > Get-Help Yorai-Levi -Examples'
    (Get-Help Yorai-Levi -Examples | Out-String).Trim()
    "    "
    $i = 1
    $examples | ForEach-Object {
        $scriptblock = $_
        $executed_code = $scriptblock.ToString().Trim()
        $output = (& $scriptblock) -join "`r`n    "
        @"
    -------------------------- EXAMPLE $i --------------------------
    
    PS > $executed_code
    $output
"@
        $i++
    } | Write-Output
    # 'NOTES'
    # "    $($Keywords -join ' ')"

    <#(Get-Help YoraiLevi -Examples | Out-String) <#-replace '\s+DESCRIPTION', '' -replace '\s+INPUTS', '' -replace '\s+OUTPUTS', '' -replace '\s+Required\?.*', '' -replace '\s+Position\?.*', '' -replace "\s+Default value\s*`n", '' -replace '\s+Accept pipeline input\?.*', '' -replace '\s+Accept wildcard characters\?.*', '' -replace "(`r`n){2,}", "`r`n" -replace "(    `r`n){2,}", "    `r`n" -split "`r*`n" | ForEach-Object {
        $_
        if ($_ -match '\s+-(?<Parameter>\w+)') {
            $set = (Get-Command YoraiLevi).Parameters[$Matches.Parameter].Attributes.ValidValues | Join-String -Separator ', '
            if (-not [String]::IsNullOrEmpty($set)) {
                "        Validate Set                 $set"
            }
        }
        
    }#>
    @"
RELATED LINKS
    resume.yorailevi.com 
    pdf.resume.yorailevi.com 
"@

}
Resume-YoraiLevi

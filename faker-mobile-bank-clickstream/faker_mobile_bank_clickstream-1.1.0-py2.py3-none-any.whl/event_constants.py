events = [
    "Login",
    "Logout",
    "ViewHome",
    "ViewAccounts",
    "ViewProducts",
    "SelectTransfer",
    "ViewTransactions",
    "ViewCreditCard",
    "ViewLoan",
    "ApplyCreditCard",
    "ApplyLoan",
    "FillCreditCardApplication",
    "FillLoanApplication",
    "SubmitCreditCardApplication",
    "SubmitLoanApplication",
    "FillTransferDetails",
    "CompleteTransfer"
]

event_details = [
    {
        "name": "Login",
        "maxCount": 1,
        "dependsOn": [] 
    },
    {
        "name": "Logout",
        "maxCount": 1,
        "dependsOn": ["Login"] 
    },
    {
        "name": "ViewHome",
        "maxCount": 4,
        "dependsOn": ["Login"] 
    },
    {
        "name": "ViewAccounts",
        "maxCount": 3,
        "dependsOn": ["Login"] 
    },
    {
        "name": "ViewProducts",
        "maxCount": 2,
        "dependsOn": ["Login"] 
    },
    {
        "name": "SelectTransfer",
        "maxCount": 3,
        "dependsOn": ["Login"] 
    },
    {
        "name": "ViewTransactions",
        "maxCount": 3,
        "dependsOn": ["ViewAccounts"] 
    },
    {
        "name": "ViewCreditCard",
        "maxCount": 2,
        "dependsOn": ["ViewProducts"] 
    },
    {
        "name": "ViewLoan",
        "maxCount": 2,
        "dependsOn": ["ViewProducts"] 
    },
    {
        "name": "ApplyCreditCard",
        "maxCount": 1,
        "dependsOn": ["ViewProducts"] 
    },
    {
        "name": "ApplyLoan",
        "maxCount": 1,
        "dependsOn": ["ViewProducts"] 
    },
    {
        "name": "FillCreditCardApplication",
        "maxCount": 1,
        "dependsOn": ["ApplyCreditCard"] 
    },
    {
        "name": "FillLoanApplication",
        "maxCount": 1,
        "dependsOn": ["ApplyLoan"] 
    },
    {
        "name": "SubmitCreditCardApplication",
        "maxCount": 1,
        "dependsOn": ["ApplyCreditCard"] 
    },
    {
        "name": "SubmitLoanApplication",
        "maxCount": 1,
        "dependsOn": ["ApplyLoan"] 
    },
    {
        "name": "FillTransferDetails",
        "maxCount": 3,
        "dependsOn": ["SelectTransfer"] 
    },
    {
        "name": "CompleteTransfer",
        "maxCount": 3,
        "dependsOn": ["FillTransferDetails"] 
    }
]
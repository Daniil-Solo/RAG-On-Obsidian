interface VendorInfo {
    name: string,
    models: Array<string>
}


const VENDORS: Array<VendorInfo> = [
    {
        name: "GigaChat",
        models: [
            "GigaChat-Lite", "GigaChat-Pro"
        ]
    },
    {
        name: "Mistral",
        models: [
            "mistral-large-latest", "ministral-3b-latest", "ministral-8b-latest", 
            "mistral-small-latest", "codestral-latest"
        ]
    },
]


export {VENDORS};
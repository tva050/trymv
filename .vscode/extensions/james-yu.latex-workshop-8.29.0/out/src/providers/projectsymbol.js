"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ProjectSymbolProvider = void 0;
const vscode = __importStar(require("vscode"));
const structure_1 = require("./structure");
class ProjectSymbolProvider {
    constructor(extension) {
        this.extension = extension;
        this.sectionNodeProvider = new structure_1.SectionNodeProvider(extension);
    }
    async provideWorkspaceSymbols() {
        const symbols = [];
        if (this.extension.manager.rootFile === undefined) {
            return symbols;
        }
        const rootFileUri = this.extension.manager.rootFileUri;
        if (rootFileUri && this.extension.lwfs.isVirtualUri(rootFileUri)) {
            return symbols;
        }
        this.sectionToSymbols(symbols, await this.sectionNodeProvider.buildLaTeXModel());
        return symbols;
    }
    sectionToSymbols(symbols, sections, containerName = 'Document') {
        sections.forEach(section => {
            const location = new vscode.Location(vscode.Uri.file(section.fileName), new vscode.Range(section.lineNumber, 0, section.toLine, 65535));
            symbols.push(new vscode.SymbolInformation(section.label, vscode.SymbolKind.String, containerName, location));
            if (section.children.length > 0) {
                this.sectionToSymbols(symbols, section.children, section.label);
            }
        });
    }
}
exports.ProjectSymbolProvider = ProjectSymbolProvider;
//# sourceMappingURL=projectsymbol.js.map
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
exports.HoverPreviewOnRefProvider = void 0;
const vscode = __importStar(require("vscode"));
const utils = __importStar(require("../../../utils/svg"));
class HoverPreviewOnRefProvider {
    constructor(extension, mj, mputils) {
        this.extension = extension;
        this.mj = mj;
        this.mputils = mputils;
    }
    async provideHoverPreviewOnRef(tex, newCommand, refData, color) {
        const md = await this.renderSvgOnRef(tex, newCommand, refData, color);
        const line = refData.position.line;
        const link = vscode.Uri.parse('command:latex-workshop.synctexto').with({ query: JSON.stringify([line, refData.file]) });
        const mdLink = new vscode.MarkdownString(`[View on pdf](${link})`);
        mdLink.isTrusted = true;
        return new vscode.Hover([this.mputils.addDummyCodeBlock(`![equation](${md})`), mdLink], tex.range);
    }
    async renderSvgOnRef(tex, newCommand, refData, color) {
        const configuration = vscode.workspace.getConfiguration('latex-workshop');
        const scale = configuration.get('hover.preview.scale');
        let newTeXString;
        if (refData.prevIndex !== undefined && configuration.get('hover.ref.number.enabled')) {
            const tag = refData.prevIndex.refNumber;
            const texString = this.replaceLabelWithTag(tex.texString, refData.label, tag);
            newTeXString = this.mputils.mathjaxify(texString, tex.envname, { stripLabel: false });
        }
        else {
            newTeXString = this.mputils.mathjaxify(tex.texString, tex.envname);
        }
        const typesetArg = newCommand + this.mputils.stripTeX(newTeXString);
        const typesetOpts = { scale, color };
        try {
            const xml = await this.mj.typeset(typesetArg, typesetOpts);
            const svg = utils.svgToDataUrl(xml);
            return svg;
        }
        catch (e) {
            this.extension.logger.logOnRejected(e);
            this.extension.logger.addLogMessage(`Error when MathJax is rendering ${typesetArg}`);
            throw e;
        }
    }
    replaceLabelWithTag(tex, refLabel, tag) {
        const texWithoutTag = tex.replace(/\\tag\{(\{[^{}]*?\}|.)*?\}/g, '');
        let newTex = texWithoutTag.replace(/\\label\{(.*?)\}/g, (_matchString, matchLabel, _offset, _s) => {
            if (refLabel) {
                if (refLabel === matchLabel) {
                    if (tag) {
                        return `\\tag{${tag}}`;
                    }
                    else {
                        return `\\tag{${matchLabel}}`;
                    }
                }
                return '\\notag';
            }
            else {
                return `\\tag{${matchLabel}}`;
            }
        });
        // To work around a bug of \tag with multi-line environments,
        // we have to put \tag after the environments.
        // See https://github.com/mathjax/MathJax/issues/1020
        newTex = newTex.replace(/(\\tag\{.*?\})([\r\n\s]*)(\\begin\{(aligned|alignedat|gathered|split)\}[^]*?\\end\{\4\})/gm, '$3$2$1');
        newTex = newTex.replace(/^\\begin\{(\w+?)\}/, '\\begin{$1*}');
        newTex = newTex.replace(/\\end\{(\w+?)\}$/, '\\end{$1*}');
        return newTex;
    }
}
exports.HoverPreviewOnRefProvider = HoverPreviewOnRefProvider;
//# sourceMappingURL=hoverpreviewonref.js.map
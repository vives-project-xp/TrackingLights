/**
 * Writes compressed C arrays of data files (web interface)
 * How to use it?
 *
 * 1) Install Node 11+ and npm
 * 2) npm install
 * 3) npm run build
 *
 * If you change data folder often, you can run it in monitoring mode (it will recompile and update *.h on every file change)
 *
 * > npm run dev
 *
 * How it works?
 *
 * It uses NodeJS packages to inline, minify and GZIP files. See writeHtmlGzipped and writeChunks invocations at the bottom of the page.
 */

const fs = require("fs");
const inliner = require("inliner");
const zlib = require("zlib");
const CleanCSS = require("clean-css");
const MinifyHTML = require("html-minifier-terser").minify;
const packageJson = require("../package.json");

/**
 *
 */
function hexdump(buffer,isHex=false) {
  let lines = [];

  for (let i = 0; i < buffer.length; i +=(isHex?32:16)) {
    var block;
    let hexArray = [];
    if (isHex) {
      block = buffer.slice(i, i + 32)
      for (let j = 0; j < block.length; j +=2 ) {
        hexArray.push("0x" + block.slice(j,j+2))
      }
    } else {
      block = buffer.slice(i, i + 16); // cut buffer into blocks of 16
      for (let value of block) {
        hexArray.push("0x" + value.toString(16).padStart(2, "0"));
      }
    }

    let hexString = hexArray.join(", ");
    let line = `  ${hexString}`;
    lines.push(line);
  }

  return lines.join(",\n");
}

function strReplace(str, search, replacement) {
  return str.split(search).join(replacement);
}

function adoptVersionAndRepo(html) {
  let repoUrl = packageJson.repository ? packageJson.repository.url : undefined;
  if (repoUrl) {
    repoUrl = repoUrl.replace(/^git\+/, "");
    repoUrl = repoUrl.replace(/\.git$/, "");
    // Replace we
    html = strReplace(html, "https://github.com/atuline/WLED", repoUrl);
    html = strReplace(html, "https://github.com/Aircoookie/WLED", repoUrl);
  }
  let version = packageJson.version;
  if (version) {
    html = strReplace(html, "##VERSION##", version);
  }
  return html;
}

function filter(str, type) {
  str = adoptVersionAndRepo(str);
  if (type === undefined) {
    return str;
  } else if (type == "css-minify") {
    return new CleanCSS({}).minify(str).styles;
  } else if (type == "js-minify") {
    return MinifyHTML('<script>' + str + '</script>', {
      collapseWhitespace: true,
      minifyJS: true, 
      continueOnParseError: false,
      removeComments: true,
    }).replace(/<[\/]*script>/g,'');
  } else if (type == "html-minify") {
    return MinifyHTML(str, {
      collapseWhitespace: true,
      maxLineLength: 80,
      minifyCSS: true,
      minifyJS: true, 
      continueOnParseError: false,
      removeComments: true,
    });
  } else if (type == "html-minify-ui") {
    return MinifyHTML(str, {
      collapseWhitespace: true,
      conservativeCollapse: true,
      maxLineLength: 80,
      minifyCSS: true,
      minifyJS: true, 
      continueOnParseError: false,
      removeComments: true,
    });
  } else {
    console.warn("Unknown filter: " + type);
    return str;
  }
}

function writeHtmlGzipped(sourceFile, resultFile, page) {
  console.info("Reading " + sourceFile);
  new inliner(sourceFile, function (error, html) {
    console.info("Inlined " + html.length + " characters");
    html = filter(html, "html-minify-ui");
    console.info("Minified to " + html.length + " characters");

    if (error) {
      console.warn(error);
      throw error;
    }

    html = adoptVersionAndRepo(html);
    zlib.gzip(html, { level: zlib.constants.Z_BEST_COMPRESSION }, function (error, result) {
      if (error) {
        console.warn(error);
        throw error;
      }

      console.info("Compressed " + result.length + " bytes");
      const array = hexdump(result);
      const src = `/*
 * Binary array for the Web UI.
 * gzip is used for smaller size and improved speeds.
 * 
 * Please see https://kno.wled.ge/advanced/custom-features/#changing-web-ui
 * to find out how to easily modify the web UI source!
 */
 
// Autogenerated from ${sourceFile}, do not edit!!
const uint16_t PAGE_${page}_L = ${result.length};
const uint8_t PAGE_${page}[] PROGMEM = {
${array}
};
`;
      console.info("Writing " + resultFile);
      fs.writeFileSync(resultFile, src);
    });
  });
}

function specToChunk(srcDir, s) {
  if (s.method == "plaintext") {
    const buf = fs.readFileSync(srcDir + "/" + s.file);
    const str = buf.toString("utf-8");
    const chunk = `
// Autogenerated from ${srcDir}/${s.file}, do not edit!!
const char ${s.name}[] PROGMEM = R"${s.prepend || ""}${filter(str, s.filter)}${
      s.append || ""
    }";

`;
    return s.mangle ? s.mangle(chunk) : chunk;
  } else if (s.method == "gzip") {
    const buf = fs.readFileSync(srcDir + "/" + s.file);
    var str = buf.toString('utf-8');
    if (s.mangle) str = s.mangle(str);
    const zip = zlib.gzipSync(filter(str, s.filter), { level: zlib.constants.Z_BEST_COMPRESSION });
    const result = hexdump(zip.toString('hex'), true);
    const chunk = `
// Autogenerated from ${srcDir}/${s.file}, do not edit!!
const uint16_t ${s.name}_length = ${zip.length};
const uint8_t ${s.name}[] PROGMEM = {
${result}
};

`;
    return chunk;
  } else if (s.method == "binary") {
    const buf = fs.readFileSync(srcDir + "/" + s.file);
    const result = hexdump(buf);
    const chunk = `
// Autogenerated from ${srcDir}/${s.file}, do not edit!!
const uint16_t ${s.name}_length = ${result.length};
const uint8_t ${s.name}[] PROGMEM = {
${result}
};

`;
    return chunk;
  } else {
    console.warn("Unknown method: " + s.method);
    return undefined;
  }
}

function writeChunks(srcDir, specs, resultFile) {
  let src = `/*
 * More web UI HTML source arrays.
 * This file is auto generated, please don't make any changes manually.
 * Instead, see https://kno.wled.ge/advanced/custom-features/#changing-web-ui
 * to find out how to easily modify the web UI source!
 */ 
`;
  specs.forEach((s) => {
    try {
      console.info("Reading " + srcDir + "/" + s.file + " as " + s.name);
      src += specToChunk(srcDir, s);
    } catch (e) {
      console.warn(
        "Failed " + s.name + " from " + srcDir + "/" + s.file,
        e.message.length > 60 ? e.message.substring(0, 60) : e.message
      );
    }
  });
  console.info("Writing " + src.length + " characters into " + resultFile);
  fs.writeFileSync(resultFile, src);
}

writeHtmlGzipped("wled00/data/index.htm", "wled00/html_ui.h", 'index');
writeHtmlGzipped("wled00/data/simple.htm", "wled00/html_simple.h", 'simple');
writeHtmlGzipped("wled00/data/pixart/pixart.htm", "wled00/html_pixart.h", 'pixart');
writeHtmlGzipped("wled00/data/cpal/cpal.htm", "wled00/html_cpal.h", 'cpal');
writeHtmlGzipped("wled00/data/pxmagic/pxmagic.htm", "wled00/html_pxmagic.h", 'pxmagic');
/*
writeChunks(
  "wled00/data",
  [
    {
      file: "simple.css",
      name: "PAGE_simpleCss",
      method: "gzip",
      filter: "css-minify",
    },
    {
      file: "simple.js",
      name: "PAGE_simpleJs",
      method: "gzip",
      filter: "js-minify",
    },
    {
      file: "simple.htm",
      name: "PAGE_simple",
      method: "gzip",
      filter: "html-minify-ui",
    }
  ],
  "wled00/html_simplex.h"
);
*/
writeChunks(
  "wled00/data",
  [
    {
      file: "style.css",
      name: "PAGE_settingsCss",
      method: "gzip",
      filter: "css-minify",
      mangle: (str) =>
        str
          .replace("%%","%")
    },
    {
      file: "settings.htm",
      name: "PAGE_settings",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "settings_wifi.htm",
      name: "PAGE_settings_wifi",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "settings_leds.htm",
      name: "PAGE_settings_leds",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "settings_dmx.htm",
      name: "PAGE_settings_dmx",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "settings_ui.htm",
      name: "PAGE_settings_ui",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "settings_sync.htm",
      name: "PAGE_settings_sync",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "settings_time.htm",
      name: "PAGE_settings_time",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "settings_sec.htm",
      name: "PAGE_settings_sec",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "settings_um.htm",
      name: "PAGE_settings_um",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "settings_2D.htm",
      name: "PAGE_settings_2D",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "settings_pin.htm",
      name: "PAGE_settings_pin",
      method: "gzip",
      filter: "html-minify"
    }
  ],
  "wled00/html_settings.h"
);

writeChunks(
  "wled00/data",
  [
    {
      file: "usermod.htm",
      name: "PAGE_usermod",
      method: "gzip",
      filter: "html-minify",
      mangle: (str) =>
        str.replace(/fetch\("http\:\/\/.*\/win/gms, 'fetch("/win'),
    },
    {
      file: "msg.htm",
      name: "PAGE_msg",
      prepend: "=====(",
      append: ")=====",
      method: "plaintext",
      filter: "html-minify",
      mangle: (str) => str.replace(/\<h2\>.*\<\/body\>/gms, "<h2>%MSG%</body>"),
    },
    {
      file: "dmxmap.htm",
      name: "PAGE_dmxmap",
      prepend: "=====(",
      append: ")=====",
      method: "plaintext",
      filter: "html-minify",
      mangle: (str) => `
#ifdef WLED_ENABLE_DMX
${str.replace(/function FM\(\)[ ]?\{/gms, "function FM() {%DMXVARS%\n")}
#else
const char PAGE_dmxmap[] PROGMEM = R"=====()=====";
#endif
`,
    },
    {
      file: "update.htm",
      name: "PAGE_update",
      method: "gzip",
      filter: "html-minify",
      mangle: (str) =>
        str
          .replace(
            /function GetV().*\<\/script\>/gms,
            "</script><script src=\"/settings/s.js?p=9\"></script>"
          )
    },
    {
      file: "welcome.htm",
      name: "PAGE_welcome",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "liveview.htm",
      name: "PAGE_liveview",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "liveviewws2D.htm",
      name: "PAGE_liveviewws2D",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "404.htm",
      name: "PAGE_404",
      method: "gzip",
      filter: "html-minify",
    },
    {
      file: "favicon.ico",
      name: "favicon",
      method: "binary",
    },
    {
      file: "iro.js",
      name: "iroJs",
      method: "gzip"
    },
    {
      file: "rangetouch.js",
      name: "rangetouchJs",
      method: "gzip"
    }
  ],
  "wled00/html_other.h"
);
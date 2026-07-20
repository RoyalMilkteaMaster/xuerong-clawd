using System;
using System.Collections;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Linq;
using System.Reflection;
using System.Web.Script.Serialization;
using System.Windows.Forms;

[assembly: AssemblyTitle("雪絨 HD 主題安裝器")]
[assembly: AssemblyDescription("將雪絨 HD 安裝到 Clawd on Desk 的使用者主題目錄")]
[assembly: AssemblyCompany("RoyalMilkteaMaster")]
[assembly: AssemblyProduct("雪絨 HD 主題安裝器")]
[assembly: AssemblyVersion("2.5.10.0")]
[assembly: AssemblyFileVersion("2.5.10.0")]

internal static class XuerongThemeInstaller
{
    private const string ThemeId = "xuerong-hd";
    private const string ResourceName = "XuerongTheme.zip";

    [STAThread]
    private static int Main(string[] args)
    {
        bool quiet = args.Any(arg => string.Equals(arg, "/quiet", StringComparison.OrdinalIgnoreCase));
        bool uninstall = args.Any(arg => string.Equals(arg, "/uninstall", StringComparison.OrdinalIgnoreCase));

        try
        {
            string userDataDirectory = GetClawdUserDataDirectory();
            string destination = Path.Combine(userDataDirectory, "themes", ThemeId);

            if (uninstall)
            {
                if (Directory.Exists(destination))
                    Directory.Delete(destination, true);
                Show(quiet, "雪絨 HD 已從 Clawd 主題清單移除。", MessageBoxIcon.Information);
                return 0;
            }

            InstallTheme(userDataDirectory, destination);
            bool clawdIsRunning = Process.GetProcessesByName("Clawd on Desk").Length > 0;
            string restartHint = clawdIsRunning
                ? "\r\n\r\nClawd 目前正在執行，請關閉後重新開啟。"
                : "\r\n\r\n開啟 Clawd 後，到「設定 → 主題」選擇「雪絨 HD」。";
            Show(quiet, "雪絨 HD 已加入 Clawd 主題清單。" + restartHint, MessageBoxIcon.Information);
            return 0;
        }
        catch (Exception error)
        {
            Show(quiet, "安裝失敗：\r\n" + error.Message, MessageBoxIcon.Error);
            return 1;
        }
    }

    private static string GetClawdUserDataDirectory()
    {
        string testRoot = Environment.GetEnvironmentVariable("XUERONG_THEME_INSTALL_ROOT");
        if (!string.IsNullOrWhiteSpace(testRoot))
            return Path.GetFullPath(testRoot);

        string appData = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
        if (string.IsNullOrWhiteSpace(appData))
            throw new InvalidOperationException("找不到 Windows 使用者資料目錄。");
        return Path.Combine(appData, "clawd-on-desk");
    }

    private static void InstallTheme(string userDataDirectory, string destination)
    {
        string themesDirectory = Path.Combine(userDataDirectory, "themes");
        Directory.CreateDirectory(themesDirectory);

        string staging = Path.Combine(themesDirectory, "." + ThemeId + ".installing-" + Guid.NewGuid().ToString("N"));
        string backup = null;

        try
        {
            Directory.CreateDirectory(staging);
            ExtractEmbeddedTheme(staging);
            ValidateTheme(staging);

            if (Directory.Exists(destination))
            {
                string backupRoot = Path.Combine(userDataDirectory, "xuerong-theme-installer-backups");
                Directory.CreateDirectory(backupRoot);
                backup = Path.Combine(backupRoot, ThemeId + "-" + DateTime.Now.ToString("yyyyMMdd-HHmmssfff"));
                Directory.Move(destination, backup);
            }

            Directory.Move(staging, destination);
        }
        catch
        {
            if (Directory.Exists(staging))
                Directory.Delete(staging, true);
            if (!Directory.Exists(destination) && backup != null && Directory.Exists(backup))
                Directory.Move(backup, destination);
            throw;
        }
    }

    private static void ExtractEmbeddedTheme(string staging)
    {
        Assembly assembly = Assembly.GetExecutingAssembly();
        using (Stream resource = assembly.GetManifestResourceStream(ResourceName))
        {
            if (resource == null)
                throw new InvalidOperationException("安裝器內缺少雪絨主題資料。");

            using (ZipArchive archive = new ZipArchive(resource, ZipArchiveMode.Read, false))
            {
                string stagingRoot = EnsureTrailingSeparator(Path.GetFullPath(staging));
                foreach (ZipArchiveEntry entry in archive.Entries)
                {
                    string relativePath = entry.FullName.Replace('/', Path.DirectorySeparatorChar);
                    if (string.IsNullOrWhiteSpace(relativePath))
                        continue;

                    string target = Path.GetFullPath(Path.Combine(staging, relativePath));
                    if (!target.StartsWith(stagingRoot, StringComparison.OrdinalIgnoreCase))
                        throw new InvalidDataException("主題壓縮檔含有不安全的路徑。");

                    if (entry.FullName.EndsWith("/", StringComparison.Ordinal))
                    {
                        Directory.CreateDirectory(target);
                        continue;
                    }

                    Directory.CreateDirectory(Path.GetDirectoryName(target));
                    using (Stream input = entry.Open())
                    using (FileStream output = new FileStream(target, FileMode.Create, FileAccess.Write, FileShare.None))
                        input.CopyTo(output);
                }
            }
        }
    }

    private static void ValidateTheme(string staging)
    {
        string themeJsonPath = Path.Combine(staging, "theme.json");
        string assetsDirectory = Path.Combine(staging, "assets");
        if (!File.Exists(themeJsonPath) || !Directory.Exists(assetsDirectory))
            throw new InvalidDataException("主題資料不完整：缺少 theme.json 或 assets 資料夾。");

        object parsed = new JavaScriptSerializer().DeserializeObject(File.ReadAllText(themeJsonPath));
        IDictionary theme = parsed as IDictionary;
        if (theme == null || !theme.Contains("name") || !theme.Contains("states"))
            throw new InvalidDataException("theme.json 格式不正確。");

        if (!File.Exists(Path.Combine(assetsDirectory, "idle.webp")))
            throw new InvalidDataException("主題資料不完整：缺少 idle.webp。");
    }

    private static string EnsureTrailingSeparator(string path)
    {
        return path.EndsWith(Path.DirectorySeparatorChar.ToString(), StringComparison.Ordinal)
            ? path
            : path + Path.DirectorySeparatorChar;
    }

    private static void Show(bool quiet, string message, MessageBoxIcon icon)
    {
        if (!quiet)
            MessageBox.Show(message, "雪絨 HD 主題安裝器", MessageBoxButtons.OK, icon);
    }
}

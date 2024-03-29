const { IgApiClient } = require("instagram-private-api");
const fs = require("fs");
const util = require("util");

const IG_USERNAME = "YourInstagramUser";
const IG_PASSWORD = "YourInstagramPassword";

const readFileAsync = util.promisify(fs.readFile);

async function login() {
  const ig = new IgApiClient();
  ig.state.generateDevice(IG_USERNAME);
  await ig.account.login(IG_USERNAME, IG_PASSWORD);
  return ig;
}

async function uploadPhoto(ig, imagePath) {
  const imageBuffer = await readFileAsync(imagePath);

  const timestamp = new Date().toLocaleString();
  const caption = `Posted with PiLaroid #piladoid #raspberrypi at ${timestamp}`;

  const publishResult = await ig.publish.photo({
    file: imageBuffer,
    caption: caption,
  });
  console.log(publishResult);
}

// Main function to execute the login and upload process
(async () => {
  try {
    // Login to Instagram
    const ig = await login();
    // Upload a photo
    await uploadPhoto(ig, process.argv[2]);
  } catch (error) {
    console.error(error);
  }
})();

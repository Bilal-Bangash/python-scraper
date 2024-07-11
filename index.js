const puppeteer = require('puppeteer')
const cheerio = require('cheerio')
const axios = require('axios')
const fs = require('fs')

// Load configuration
const config = JSON.parse(fs.readFileSync('config.json'))

console.log('%cconfig', 'color:red;font-size:50px', config)

async function scrapeAmazon(searchQuery) {
  const { urlTemplate, selectors, baseUrl, nextPageDisabled } = config.amazon
  return scrape(urlTemplate, searchQuery, selectors, baseUrl, nextPageDisabled)
}

async function scrapeMacys(searchQuery) {
  const { urlTemplate, selectors, baseUrl, nextPageDisabled } = config.macys
  return scrape(urlTemplate, searchQuery, selectors, baseUrl, nextPageDisabled)
}

async function scrapeEtsy(searchQuery) {
  const { urlTemplate, selectors, baseUrl, nextPageDisabled } = config.etsy
  return scrape(urlTemplate, searchQuery, selectors, baseUrl, nextPageDisabled)
}

async function scrape(
  urlTemplate,
  searchQuery,
  selectors,
  baseUrl,
  nextPageDisabled
) {
  let page = 1
  let results = []

  const browser = await puppeteer.launch({ headless: false })
  const pageObject = await browser.newPage()

  while (results.length < 10) {
    const url = urlTemplate
      .replace('{searchQuery}', searchQuery)
      .replace('{page}', page)
    await pageObject.goto(url, { waitUntil: 'networkidle2' })

    const content = await pageObject.content()
    const $ = cheerio.load(content)

    const mainContainer = $(selectors.mainContainer)
    const products = mainContainer.find(selectors.productContainer)

    if (products.length === 0 || $(nextPageDisabled).length > 0) break

    products.each((index, element) => {
      const title = $(element).find(selectors.title).text().trim()
      const price = $(element).find(selectors.price).text().trim()
      const link = baseUrl + $(element).find(selectors.link).attr('href')
      const image = $(element).find(selectors.image).attr('src')

      results.push({ title, price, link, image })
    })

    page++
    await randomDelay()
  }

  await browser.close()
  return results
}

function randomDelay() {
  return new Promise((resolve) =>
    setTimeout(resolve, Math.floor(Math.random() * 5000))
  )
}

// Example usage
const scrapeProducts = async () => {
  const amazonResults = await scrapeAmazon('laptop')
  fs.writeFileSync('amazonResults.json', JSON.stringify(amazonResults))

  const macysResults = await scrapeMacys('shirt')
  fs.writeFileSync('macysResults.json', JSON.stringify(macysResults))

  const etsyResults = await scrapeEtsy('handmade necklace')
  fs.writeFileSync('etsyResults.json', JSON.stringify(etsyResults))
}
scrapeProducts()

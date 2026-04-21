import { toPng } from 'html-to-image'

export async function exportElementAsPng(el: HTMLElement, filename: string): Promise<void> {
  const dataUrl = await toPng(el, {
    pixelRatio: 2,
    backgroundColor: '#f3ece1',
    cacheBust: true,
  })
  const link = document.createElement('a')
  link.href = dataUrl
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

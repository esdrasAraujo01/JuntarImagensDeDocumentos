// Image processing utilities for perspective correction and image combination

/**
 * Applies perspective correction to an image based on four corner points
 * @param {string} imageUrl - URL of the source image
 * @param {Array} points - Array of 4 points in format [{x, y}, ...] where x,y are 0-1 normalized
 * @returns {Promise<string>} - Data URL of the corrected image
 */
export async function correctPerspective(imageUrl, points) {
  return new Promise((resolve, reject) => {
    if (points.length !== 4) {
      reject(new Error('Exactly 4 points are required for perspective correction'))
      return
    }

    const img = new Image()
    img.crossOrigin = 'anonymous'
    
    img.onload = () => {
      try {
        // Convert normalized points to actual pixel coordinates
        const actualPoints = points.map(point => ({
          x: point.x * img.width,
          y: point.y * img.height
        }))

        // Calculate the dimensions of the output rectangle
        const width1 = distance(actualPoints[0], actualPoints[1])
        const width2 = distance(actualPoints[2], actualPoints[3])
        const height1 = distance(actualPoints[0], actualPoints[3])
        const height2 = distance(actualPoints[1], actualPoints[2])
        
        const outputWidth = Math.max(width1, width2)
        const outputHeight = Math.max(height1, height2)

        // Create canvas for the corrected image
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')
        canvas.width = outputWidth
        canvas.height = outputHeight

        // Define destination points (rectangle corners)
        const destPoints = [
          { x: 0, y: 0 },
          { x: outputWidth, y: 0 },
          { x: outputWidth, y: outputHeight },
          { x: 0, y: outputHeight }
        ]

        // Apply perspective transformation using multiple triangular patches
        // This is a simplified approach - for better results, we'd use a proper perspective transform
        applyPerspectiveTransform(ctx, img, actualPoints, destPoints, outputWidth, outputHeight)

        resolve(canvas.toDataURL('image/png'))
      } catch (error) {
        reject(error)
      }
    }

    img.onerror = () => reject(new Error('Failed to load image'))
    img.src = imageUrl
  })
}

/**
 * Combines two images horizontally or vertically
 * @param {string} image1Url - URL of the first image
 * @param {string} image2Url - URL of the second image
 * @param {Object} options - Combination options
 * @returns {Promise<string>} - Data URL of the combined image
 */
export async function combineImages(image1Url, image2Url, options = {}) {
  const {
    orientation = 'horizontal',
    alignment = 'center',
    overlap = 0
  } = options

  return new Promise((resolve, reject) => {
    let loadedImages = 0
    const images = [new Image(), new Image()]
    
    const onImageLoad = () => {
      loadedImages++
      if (loadedImages === 2) {
        try {
          const result = performImageCombination(images[0], images[1], orientation, alignment, overlap)
          resolve(result)
        } catch (error) {
          reject(error)
        }
      }
    }

    images.forEach((img, index) => {
      img.crossOrigin = 'anonymous'
      img.onload = onImageLoad
      img.onerror = () => reject(new Error(`Failed to load image ${index + 1}`))
    })

    images[0].src = image1Url
    images[1].src = image2Url
  })
}

/**
 * Calculate distance between two points
 */
function distance(p1, p2) {
  return Math.sqrt(Math.pow(p2.x - p1.x, 2) + Math.pow(p2.y - p1.y, 2))
}

/**
 * Apply perspective transformation using a grid-based approach
 */
function applyPerspectiveTransform(ctx, img, srcPoints, destPoints, outputWidth, outputHeight) {
  // Clear the canvas
  ctx.clearRect(0, 0, outputWidth, outputHeight)
  
  // For a simplified perspective correction, we'll use a grid-based approach
  // This divides the quadrilateral into smaller triangles and transforms each
  const gridSize = 20
  
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      const u1 = i / gridSize
      const v1 = j / gridSize
      const u2 = (i + 1) / gridSize
      const v2 = (j + 1) / gridSize
      
      // Calculate source quad for this grid cell
      const srcQuad = [
        bilinearInterpolate(srcPoints, u1, v1),
        bilinearInterpolate(srcPoints, u2, v1),
        bilinearInterpolate(srcPoints, u2, v2),
        bilinearInterpolate(srcPoints, u1, v2)
      ]
      
      // Calculate destination quad for this grid cell
      const destQuad = [
        bilinearInterpolate(destPoints, u1, v1),
        bilinearInterpolate(destPoints, u2, v1),
        bilinearInterpolate(destPoints, u2, v2),
        bilinearInterpolate(destPoints, u1, v2)
      ]
      
      // Draw this grid cell
      drawQuadrilateral(ctx, img, srcQuad, destQuad)
    }
  }
}

/**
 * Bilinear interpolation between four corner points
 */
function bilinearInterpolate(points, u, v) {
  const [p0, p1, p2, p3] = points
  
  // Interpolate along top edge
  const top = {
    x: p0.x * (1 - u) + p1.x * u,
    y: p0.y * (1 - u) + p1.y * u
  }
  
  // Interpolate along bottom edge
  const bottom = {
    x: p3.x * (1 - u) + p2.x * u,
    y: p3.y * (1 - u) + p2.y * u
  }
  
  // Interpolate between top and bottom
  return {
    x: top.x * (1 - v) + bottom.x * v,
    y: top.y * (1 - v) + bottom.y * v
  }
}

/**
 * Draw a quadrilateral patch from source to destination
 */
function drawQuadrilateral(ctx, img, srcQuad, destQuad) {
  // This is a simplified approach - we'll draw two triangles to approximate the quad
  
  // First triangle: 0-1-2
  drawTriangle(ctx, img, 
    [srcQuad[0], srcQuad[1], srcQuad[2]], 
    [destQuad[0], destQuad[1], destQuad[2]]
  )
  
  // Second triangle: 0-2-3
  drawTriangle(ctx, img, 
    [srcQuad[0], srcQuad[2], srcQuad[3]], 
    [destQuad[0], destQuad[2], destQuad[3]]
  )
}

/**
 * Draw a triangular patch from source to destination
 */
function drawTriangle(ctx, img, srcTriangle, destTriangle) {
  ctx.save()
  
  // Create clipping path for destination triangle
  ctx.beginPath()
  ctx.moveTo(destTriangle[0].x, destTriangle[0].y)
  ctx.lineTo(destTriangle[1].x, destTriangle[1].y)
  ctx.lineTo(destTriangle[2].x, destTriangle[2].y)
  ctx.closePath()
  ctx.clip()
  
  // Calculate transformation matrix for this triangle
  const transform = calculateTriangleTransform(srcTriangle, destTriangle)
  
  if (transform) {
    ctx.setTransform(transform.a, transform.b, transform.c, transform.d, transform.e, transform.f)
    ctx.drawImage(img, 0, 0)
  }
  
  ctx.restore()
}

/**
 * Calculate transformation matrix for mapping one triangle to another
 */
function calculateTriangleTransform(src, dest) {
  // This is a simplified transformation - for production use, implement proper affine transform
  try {
    const [s0, s1, s2] = src
    const [d0, d1, d2] = dest
    
    // Calculate scale and translation (simplified)
    const scaleX = (d1.x - d0.x) / (s1.x - s0.x) || 1
    const scaleY = (d1.y - d0.y) / (s1.y - s0.y) || 1
    const translateX = d0.x - s0.x * scaleX
    const translateY = d0.y - s0.y * scaleY
    
    return {
      a: scaleX,
      b: 0,
      c: 0,
      d: scaleY,
      e: translateX,
      f: translateY
    }
  } catch (error) {
    return null
  }
}

/**
 * Perform the actual image combination
 */
function performImageCombination(img1, img2, orientation, alignment, overlap) {
  let canvas, ctx, totalWidth, totalHeight
  
  if (orientation === 'horizontal') {
    // Resize images to same height
    const targetHeight = Math.max(img1.height, img2.height)
    const img1Width = (img1.width * targetHeight) / img1.height
    const img2Width = (img2.width * targetHeight) / img2.height
    
    totalWidth = img1Width + img2Width - overlap
    totalHeight = targetHeight
    
    canvas = document.createElement('canvas')
    ctx = canvas.getContext('2d')
    canvas.width = totalWidth
    canvas.height = totalHeight
    
    // Draw first image
    ctx.drawImage(img1, 0, 0, img1Width, targetHeight)
    
    // Draw second image with overlap
    const img2X = img1Width - overlap
    
    if (overlap > 0) {
      // Apply blending for overlap area
      ctx.globalAlpha = 0.5
      ctx.drawImage(img2, img2X, 0, img2Width, targetHeight)
      ctx.globalAlpha = 1.0
    } else {
      ctx.drawImage(img2, img2X, 0, img2Width, targetHeight)
    }
    
  } else {
    // Vertical combination
    const targetWidth = Math.max(img1.width, img2.width)
    const img1Height = (img1.height * targetWidth) / img1.width
    const img2Height = (img2.height * targetWidth) / img2.width
    
    totalWidth = targetWidth
    totalHeight = img1Height + img2Height - overlap
    
    canvas = document.createElement('canvas')
    ctx = canvas.getContext('2d')
    canvas.width = totalWidth
    canvas.height = totalHeight
    
    // Draw first image
    ctx.drawImage(img1, 0, 0, targetWidth, img1Height)
    
    // Draw second image with overlap
    const img2Y = img1Height - overlap
    
    if (overlap > 0) {
      // Apply blending for overlap area
      ctx.globalAlpha = 0.5
      ctx.drawImage(img2, 0, img2Y, targetWidth, img2Height)
      ctx.globalAlpha = 1.0
    } else {
      ctx.drawImage(img2, 0, img2Y, targetWidth, img2Height)
    }
  }
  
  return canvas.toDataURL('image/png')
}

/**
 * Download an image from a data URL
 * @param {string} dataUrl - Data URL of the image
 * @param {string} filename - Desired filename
 */
export function downloadImage(dataUrl, filename = 'processed-image.png') {
  const link = document.createElement('a')
  link.download = filename
  link.href = dataUrl
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}


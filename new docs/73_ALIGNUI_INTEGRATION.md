# 73_ALIGNUI_INTEGRATION.md

## AlignUI: Screen Element Detection & Automation

### What is AlignUI?

```
AlignUI = AI-powered screen element detection

Purpose:
- Detect buttons, text fields, images on device screen
- Get exact coordinates of UI elements
- Automate clicks and interactions
- Works without knowing app structure

Benefits:
✅ No app inspection needed
✅ Works with any app (even proprietary)
✅ Robust to UI changes
✅ Computer vision powered
✅ Fast element detection (<500ms)

How it works:
1. Take screenshot of device
2. Send to AlignUI API
3. Get back element locations & types
4. Click/interact with detected elements
```

### AlignUI JavaScript Library

```typescript
// src/services/alignui.ts
import axios from 'axios'

interface DetectedElement {
  id: string
  type: 'button' | 'text' | 'image' | 'input' | 'checkbox' | 'other'
  label: string
  coordinates: {
    x: number
    y: number
    width: number
    height: number
  }
  confidence: number  // 0-1
  description: string
}

class AlignUIService {
  private apiKey: string
  private apiUrl: string = 'https://api.alignui.com'
  
  constructor(apiKey: string) {
    this.apiKey = apiKey
  }
  
  /**
   * Detect elements in a screenshot
   */
  async detectElements(
    screenshotPath: string,
    options?: {
      includeText?: boolean
      includeImages?: boolean
      minConfidence?: number
    }
  ): Promise<DetectedElement[]> {
    const formData = new FormData()
    
    // Read image file
    const file = await fetch(screenshotPath).then(r => r.blob())
    formData.append('image', file)
    
    // Add options
    if (options?.includeText !== undefined) {
      formData.append('include_text', options.includeText.toString())
    }
    if (options?.includeImages !== undefined) {
      formData.append('include_images', options.includeImages.toString())
    }
    if (options?.minConfidence !== undefined) {
      formData.append('min_confidence', options.minConfidence.toString())
    }
    
    try {
      const response = await axios.post(
        `${this.apiUrl}/detect`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'multipart/form-data',
          },
        }
      )
      
      return response.data.elements
    } catch (error) {
      console.error('AlignUI detection failed:', error)
      throw error
    }
  }
  
  /**
   * Find element by label/text
   */
  async findElement(
    screenshotPath: string,
    label: string
  ): Promise<DetectedElement | null> {
    const elements = await this.detectElements(screenshotPath)
    
    // Find best match
    return elements.find(el => 
      el.label.toLowerCase().includes(label.toLowerCase())
    ) || null
  }
  
  /**
   * Click on detected element
   */
  async clickElement(
    deviceId: string,
    element: DetectedElement
  ): Promise<boolean> {
    try {
      // Calculate center of element
      const x = element.coordinates.x + element.coordinates.width / 2
      const y = element.coordinates.y + element.coordinates.height / 2
      
      // Send click command to device via ADB
      const response = await axios.post('/api/device/click', {
        deviceId,
        x,
        y,
      })
      
      return response.data.success
    } catch (error) {
      console.error('Click failed:', error)
      return false
    }
  }
  
  /**
   * Type text into detected input field
   */
  async typeIntoElement(
    deviceId: string,
    element: DetectedElement,
    text: string
  ): Promise<boolean> {
    try {
      // First click on the element
      await this.clickElement(deviceId, element)
      
      // Then type text
      const response = await axios.post('/api/device/type', {
        deviceId,
        text,
      })
      
      return response.data.success
    } catch (error) {
      console.error('Type failed:', error)
      return false
    }
  }
  
  /**
   * Extract text from screenshot
   */
  async extractText(screenshotPath: string): Promise<string> {
    const formData = new FormData()
    const file = await fetch(screenshotPath).then(r => r.blob())
    formData.append('image', file)
    
    try {
      const response = await axios.post(
        `${this.apiUrl}/ocr`,
        formData,
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'multipart/form-data',
          },
        }
      )
      
      return response.data.text
    } catch (error) {
      console.error('OCR failed:', error)
      throw error
    }
  }
}

export { AlignUIService, DetectedElement }
```

### Automation with AlignUI

```typescript
// src/services/automate.ts
import { AlignUIService } from './alignui'
import { ADBConnectionManager } from './adb'

class AutomationEngine {
  private alignui: AlignUIService
  private adb: ADBConnectionManager
  
  constructor(alignuiKey: string) {
    this.alignui = new AlignUIService(alignuiKey)
    this.adb = new ADBConnectionManager()
  }
  
  /**
   * Execute automation script
   */
  async executeScript(
    deviceId: string,
    script: AutomationStep[]
  ): Promise<AutomationResult> {
    const results: StepResult[] = []
    
    for (const step of script) {
      console.log(`Executing: ${step.action}`)
      
      try {
        const result = await this.executeStep(deviceId, step)
        results.push(result)
        
        if (!result.success) {
          console.warn(`Step failed: ${result.error}`)
          if (step.stopOnError) break
        }
      } catch (error) {
        results.push({
          step: step.id,
          success: false,
          error: error.message,
        })
        
        if (step.stopOnError) break
      }
      
      // Add delay between steps
      await new Promise(resolve =>
        setTimeout(resolve, step.delay || 500)
      )
    }
    
    return {
      deviceId,
      totalSteps: script.length,
      completedSteps: results.filter(r => r.success).length,
      results,
    }
  }
  
  private async executeStep(
    deviceId: string,
    step: AutomationStep
  ): Promise<StepResult> {
    switch (step.action) {
      case 'screenshot':
        return await this.takeScreenshot(deviceId, step)
      
      case 'click':
        return await this.clickElement(deviceId, step)
      
      case 'type':
        return await this.typeText(deviceId, step)
      
      case 'find':
        return await this.findElement(deviceId, step)
      
      case 'verify':
        return await this.verifyElement(deviceId, step)
      
      case 'wait':
        return await this.wait(step)
      
      default:
        return {
          step: step.id,
          success: false,
          error: `Unknown action: ${step.action}`,
        }
    }
  }
  
  private async takeScreenshot(
    deviceId: string,
    step: AutomationStep
  ): Promise<StepResult> {
    try {
      const path = await this.adb.takeScreenshot(deviceId)
      return {
        step: step.id,
        success: true,
        data: { path },
      }
    } catch (error) {
      return {
        step: step.id,
        success: false,
        error: error.message,
      }
    }
  }
  
  private async clickElement(
    deviceId: string,
    step: AutomationStep
  ): Promise<StepResult> {
    try {
      // Take screenshot first
      const screenshotPath = await this.adb.takeScreenshot(deviceId)
      
      // Find element
      const element = await this.alignui.findElement(
        screenshotPath,
        step.params.label
      )
      
      if (!element) {
        return {
          step: step.id,
          success: false,
          error: `Element not found: ${step.params.label}`,
        }
      }
      
      // Click element
      const success = await this.alignui.clickElement(deviceId, element)
      
      return {
        step: step.id,
        success,
        data: { element },
      }
    } catch (error) {
      return {
        step: step.id,
        success: false,
        error: error.message,
      }
    }
  }
  
  private async typeText(
    deviceId: string,
    step: AutomationStep
  ): Promise<StepResult> {
    try {
      const screenshotPath = await this.adb.takeScreenshot(deviceId)
      
      // Find input field
      const element = await this.alignui.findElement(
        screenshotPath,
        step.params.target
      )
      
      if (!element) {
        return {
          step: step.id,
          success: false,
          error: `Input field not found: ${step.params.target}`,
        }
      }
      
      // Type text
      const success = await this.alignui.typeIntoElement(
        deviceId,
        element,
        step.params.text
      )
      
      return {
        step: step.id,
        success,
      }
    } catch (error) {
      return {
        step: step.id,
        success: false,
        error: error.message,
      }
    }
  }
  
  private async findElement(
    deviceId: string,
    step: AutomationStep
  ): Promise<StepResult> {
    try {
      const screenshotPath = await this.adb.takeScreenshot(deviceId)
      
      const element = await this.alignui.findElement(
        screenshotPath,
        step.params.label
      )
      
      return {
        step: step.id,
        success: !!element,
        data: { element },
      }
    } catch (error) {
      return {
        step: step.id,
        success: false,
        error: error.message,
      }
    }
  }
  
  private async verifyElement(
    deviceId: string,
    step: AutomationStep
  ): Promise<StepResult> {
    // Similar to findElement
    return this.findElement(deviceId, step)
  }
  
  private async wait(step: AutomationStep): Promise<StepResult> {
    return new Promise(resolve => {
      setTimeout(() => {
        resolve({
          step: step.id,
          success: true,
        })
      }, step.params.duration || 1000)
    })
  }
}

// Types
interface AutomationStep {
  id: string
  action: 'screenshot' | 'click' | 'type' | 'find' | 'verify' | 'wait'
  params: Record<string, any>
  delay?: number
  stopOnError?: boolean
}

interface StepResult {
  step: string
  success: boolean
  error?: string
  data?: Record<string, any>
}

interface AutomationResult {
  deviceId: string
  totalSteps: number
  completedSteps: number
  results: StepResult[]
}

export { AutomationEngine, AutomationStep, AutomationResult }
```

### Frontend Integration

```typescript
// src/components/AutomationBuilder/ScriptEditor.tsx
import React, { useState } from 'react'
import { AutomationEngine, AutomationStep } from '../../services/automate'

export default function ScriptEditor() {
  const [script, setScript] = useState<AutomationStep[]>([
    {
      id: '1',
      action: 'screenshot',
      params: {},
    },
    {
      id: '2',
      action: 'click',
      params: { label: 'Send' },
      delay: 500,
    },
  ])
  
  const [executing, setExecuting] = useState(false)
  const [results, setResults] = useState(null)
  
  const executeScript = async (deviceId: string) => {
    setExecuting(true)
    
    try {
      const engine = new AutomationEngine(process.env.REACT_APP_ALIGNUI_KEY || '')
      const result = await engine.executeScript(deviceId, script)
      setResults(result)
    } catch (error) {
      console.error('Script execution failed:', error)
    } finally {
      setExecuting(false)
    }
  }
  
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-bold">Automation Script</h2>
      
      {/* Script Steps */}
      <div className="border rounded p-4 space-y-2">
        {script.map((step, idx) => (
          <div key={step.id} className="flex gap-2 p-2 bg-gray-50 rounded">
            <span className="font-mono text-sm">{idx + 1}.</span>
            <div className="flex-1">
              <span className="font-semibold">{step.action}</span>
              {Object.entries(step.params).length > 0 && (
                <div className="text-sm text-gray-600">
                  {JSON.stringify(step.params)}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      
      {/* Execute Button */}
      <button
        onClick={() => executeScript('device1')}
        disabled={executing}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {executing ? 'Executing...' : 'Execute Script'}
      </button>
      
      {/* Results */}
      {results && (
        <div className="border rounded p-4 bg-green-50">
          <h3 className="font-semibold mb-2">Results</h3>
          <p className="text-sm">
            Completed: {results.completedSteps}/{results.totalSteps}
          </p>
        </div>
      )}
    </div>
  )
}
```

---

## End of 73_ALIGNUI_INTEGRATION.md
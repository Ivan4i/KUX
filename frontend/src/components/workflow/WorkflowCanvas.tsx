import { useCallback, useState, useEffect } from 'react'
import ReactFlow, {
  Node,
  Edge,
  Controls,
  Background,
  MiniMap,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  NodeTypes,
  BackgroundVariant,
  Panel,
} from 'reactflow'
import 'reactflow/dist/style.css'
import { RiSaveLine, RiPlayLine, RiDeleteBinLine, RiLoader4Line } from '@remixicon/react'
import toast from 'react-hot-toast'

import { TriggerNode } from './nodes/TriggerNode'
import { ActionNode } from './nodes/ActionNode'
import { ConditionNode } from './nodes/ConditionNode'
import { NodePalette } from './NodePalette'
import {
  getWorkflow,
  createWorkflow,
  updateWorkflow,
  runWorkflow,
  type WorkflowNode,
  type WorkflowEdge,
} from '@/services/api'

// Define node types
const nodeTypes: NodeTypes = {
  trigger: TriggerNode,
  action: ActionNode,
  condition: ConditionNode,
}

// Default empty canvas nodes for new workflow
const defaultNodes: Node[] = []
const defaultEdges: Edge[] = []

// Demo nodes for when no workflow is loaded
const demoNodes: Node[] = [
  {
    id: 'trigger-1',
    type: 'trigger',
    position: { x: 250, y: 50 },
    data: {
      label: 'Fetch from Notion',
      description: 'Get pending leads',
      icon: 'notion',
    },
  },
  {
    id: 'action-1',
    type: 'action',
    position: { x: 250, y: 180 },
    data: {
      label: 'Analyze with Gemini',
      description: 'Generate personalized message',
      icon: 'gemini',
      agent: 'gemini',
    },
  },
  {
    id: 'condition-1',
    type: 'condition',
    position: { x: 250, y: 320 },
    data: {
      label: 'Has Phone?',
      description: 'Check if lead has phone number',
      condition: 'lead.phone != null',
    },
  },
  {
    id: 'action-2',
    type: 'action',
    position: { x: 100, y: 460 },
    data: {
      label: 'Send WhatsApp',
      description: 'Send message via WhatsApp',
      icon: 'whatsapp',
      agent: 'whatsapp',
    },
  },
  {
    id: 'action-3',
    type: 'action',
    position: { x: 400, y: 460 },
    data: {
      label: 'Send SMS',
      description: 'Send message via SMS',
      icon: 'sms',
      agent: 'sms',
    },
  },
]

const demoEdges: Edge[] = [
  {
    id: 'e1-2',
    source: 'trigger-1',
    target: 'action-1',
    animated: true,
  },
  {
    id: 'e2-3',
    source: 'action-1',
    target: 'condition-1',
  },
  {
    id: 'e3-4',
    source: 'condition-1',
    target: 'action-2',
    sourceHandle: 'yes',
    label: 'Yes',
    style: { stroke: '#10b981' },
  },
  {
    id: 'e3-5',
    source: 'condition-1',
    target: 'action-3',
    sourceHandle: 'no',
    label: 'No',
    style: { stroke: '#ef4444' },
  },
]

interface WorkflowCanvasProps {
  /** Workflow ID to load (for editing existing workflow) */
  workflowId?: string
  /** Name for new workflow (when creating) */
  workflowName?: string
  /** Description for new workflow */
  workflowDescription?: string
  /** Show demo nodes when no workflow loaded */
  showDemo?: boolean
  /** Callback when workflow is saved (returns workflow ID) */
  onSave?: (nodes: Node[], edges: Edge[]) => void
  /** Callback when workflow run is triggered */
  onRun?: () => void
  /** Callback when workflow is created/updated (returns workflow data) */
  onWorkflowSaved?: (workflow: { id: string; name: string }) => void
}

export function WorkflowCanvas({
  workflowId,
  workflowName = 'Untitled Workflow',
  workflowDescription,
  showDemo = true,
  onSave,
  onRun,
  onWorkflowSaved,
}: WorkflowCanvasProps) {
  const [currentWorkflowId, setCurrentWorkflowId] = useState<string | null>(workflowId || null)
  const [currentWorkflowName, setCurrentWorkflowName] = useState(workflowName)
  const [nodes, setNodes, onNodesChange] = useNodesState(showDemo ? demoNodes : defaultNodes)
  const [edges, setEdges, onEdgesChange] = useEdgesState(showDemo ? demoEdges : defaultEdges)
  const [selectedNodes, setSelectedNodes] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [isRunning, setIsRunning] = useState(false)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)

  // Load workflow when workflowId changes
  useEffect(() => {
    if (workflowId) {
      loadWorkflow(workflowId)
    }
  }, [workflowId])

  // Track unsaved changes
  useEffect(() => {
    setHasUnsavedChanges(true)
  }, [nodes, edges])

  // Load existing workflow from API
  const loadWorkflow = async (id: string) => {
    try {
      setIsLoading(true)
      const workflow = await getWorkflow(id)

      // Convert API format to ReactFlow format
      const loadedNodes: Node[] = workflow.nodes.map((n: WorkflowNode) => ({
        id: n.id,
        type: n.type,
        position: n.position,
        data: n.data,
      }))

      const loadedEdges: Edge[] = workflow.edges.map((e: WorkflowEdge) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        sourceHandle: e.sourceHandle || undefined,
        targetHandle: e.targetHandle || undefined,
        label: e.label || undefined,
        animated: e.animated || false,
        style: e.style || undefined,
      }))

      setNodes(loadedNodes)
      setEdges(loadedEdges)
      setCurrentWorkflowId(workflow.id)
      setCurrentWorkflowName(workflow.name)
      setHasUnsavedChanges(false)

      toast.success(`Loaded workflow: ${workflow.name}`)
    } catch (error) {
      console.error('Error loading workflow:', error)
      toast.error('Failed to load workflow')
    } finally {
      setIsLoading(false)
    }
  }

  // Handle new connections
  const onConnect = useCallback(
    (params: Connection) => {
      setEdges((eds) => addEdge({ ...params, animated: true }, eds))
    },
    [setEdges]
  )

  // Handle node selection
  const onSelectionChange = useCallback(
    ({ nodes: selectedNodes }: { nodes: Node[] }) => {
      setSelectedNodes(selectedNodes.map((n) => n.id))
    },
    []
  )

  // Handle drop from palette
  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault()

      const type = event.dataTransfer.getData('application/reactflow')
      const nodeDataStr = event.dataTransfer.getData('application/nodedata')

      if (!type || !nodeDataStr) return

      const nodeData = JSON.parse(nodeDataStr)

      const position = {
        x: event.clientX - 250,
        y: event.clientY - 100,
      }

      const newNode: Node = {
        id: `${type}-${Date.now()}`,
        type,
        position,
        data: nodeData,
      }

      setNodes((nds) => [...nds, newNode])
    },
    [setNodes]
  )

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
  }, [])

  // Delete selected nodes
  const deleteSelected = useCallback(() => {
    setNodes((nds) => nds.filter((n) => !selectedNodes.includes(n.id)))
    setEdges((eds) => eds.filter((e) =>
      !selectedNodes.includes(e.source) && !selectedNodes.includes(e.target)
    ))
    setSelectedNodes([])
  }, [selectedNodes, setNodes, setEdges])

  // Save workflow to API
  const handleSave = useCallback(async () => {
    try {
      setIsSaving(true)

      // Convert ReactFlow format to API format
      const apiNodes: WorkflowNode[] = nodes.map((n) => ({
        id: n.id,
        type: n.type || 'action',
        position: n.position,
        data: n.data || {},
      }))

      const apiEdges: WorkflowEdge[] = edges.map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        sourceHandle: e.sourceHandle || null,
        targetHandle: e.targetHandle || null,
        label: typeof e.label === 'string' ? e.label : null,
        animated: e.animated || false,
        style: e.style || null,
      }))

      let savedWorkflow

      if (currentWorkflowId) {
        // Update existing workflow
        savedWorkflow = await updateWorkflow(currentWorkflowId, {
          nodes: apiNodes,
          edges: apiEdges,
        })
        toast.success('Workflow saved!')
      } else {
        // Create new workflow
        savedWorkflow = await createWorkflow({
          name: currentWorkflowName,
          description: workflowDescription,
          nodes: apiNodes,
          edges: apiEdges,
        })
        setCurrentWorkflowId(savedWorkflow.id)
        toast.success('Workflow created!')
      }

      setHasUnsavedChanges(false)

      // Call callbacks
      if (onSave) {
        onSave(nodes, edges)
      }
      if (onWorkflowSaved && savedWorkflow) {
        onWorkflowSaved({ id: savedWorkflow.id, name: savedWorkflow.name })
      }
    } catch (error) {
      console.error('Error saving workflow:', error)
      toast.error('Failed to save workflow')
    } finally {
      setIsSaving(false)
    }
  }, [nodes, edges, currentWorkflowId, currentWorkflowName, workflowDescription, onSave, onWorkflowSaved])

  // Run workflow
  const handleRun = useCallback(async () => {
    // Save first if there are unsaved changes
    if (hasUnsavedChanges || !currentWorkflowId) {
      await handleSave()
    }

    if (!currentWorkflowId) {
      toast.error('Please save the workflow first')
      return
    }

    try {
      setIsRunning(true)
      await runWorkflow(currentWorkflowId)
      toast.success('Workflow started!')

      if (onRun) {
        onRun()
      }
    } catch (error) {
      console.error('Error running workflow:', error)
      toast.error('Failed to start workflow')
    } finally {
      setIsRunning(false)
    }
  }, [currentWorkflowId, hasUnsavedChanges, handleSave, onRun])

  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-200px)] bg-gray-50 rounded-lg border border-gray-200 items-center justify-center">
        <div className="flex items-center gap-2 text-gray-500">
          <RiLoader4Line className="size-5 animate-spin" />
          Loading workflow...
        </div>
      </div>
    )
  }

  return (
    <div className="flex h-[calc(100vh-200px)] bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
      {/* Node Palette Sidebar */}
      <NodePalette />

      {/* Canvas */}
      <div className="flex-1" onDrop={onDrop} onDragOver={onDragOver}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          onSelectionChange={onSelectionChange}
          nodeTypes={nodeTypes}
          fitView
          snapToGrid
          snapGrid={[15, 15]}
          defaultEdgeOptions={{
            style: { strokeWidth: 2, stroke: '#94a3b8' },
            type: 'smoothstep',
          }}
        >
          <Controls />
          <MiniMap
            nodeColor={(node) => {
              switch (node.type) {
                case 'trigger': return '#8b5cf6'
                case 'action': return '#3b82f6'
                case 'condition': return '#f59e0b'
                default: return '#94a3b8'
              }
            }}
            maskColor="rgba(0, 0, 0, 0.1)"
          />
          <Background variant={BackgroundVariant.Dots} gap={20} size={1} />

          {/* Top Panel with Actions */}
          <Panel position="top-right" className="flex gap-2">
            {selectedNodes.length > 0 && (
              <button
                onClick={deleteSelected}
                className="flex items-center gap-2 px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors text-sm"
              >
                <RiDeleteBinLine className="size-4" />
                Delete ({selectedNodes.length})
              </button>
            )}
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="flex items-center gap-2 px-3 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm disabled:opacity-50"
            >
              {isSaving ? (
                <RiLoader4Line className="size-4 animate-spin" />
              ) : (
                <RiSaveLine className="size-4" />
              )}
              {hasUnsavedChanges ? 'Save*' : 'Save'}
            </button>
            <button
              onClick={handleRun}
              disabled={isRunning || nodes.length === 0}
              className="flex items-center gap-2 px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm disabled:opacity-50"
            >
              {isRunning ? (
                <RiLoader4Line className="size-4 animate-spin" />
              ) : (
                <RiPlayLine className="size-4" />
              )}
              Run
            </button>
          </Panel>

          {/* Top-left info panel */}
          <Panel position="top-left" className="bg-white/90 backdrop-blur-sm rounded-lg px-3 py-2 shadow-sm border border-gray-200">
            <div className="text-sm font-medium text-gray-900">{currentWorkflowName}</div>
            <div className="text-xs text-gray-500">
              {nodes.length} nodes, {edges.length} connections
              {currentWorkflowId && <span className="ml-2 text-green-600">(saved)</span>}
              {!currentWorkflowId && <span className="ml-2 text-amber-600">(unsaved)</span>}
            </div>
          </Panel>
        </ReactFlow>
      </div>
    </div>
  )
}
